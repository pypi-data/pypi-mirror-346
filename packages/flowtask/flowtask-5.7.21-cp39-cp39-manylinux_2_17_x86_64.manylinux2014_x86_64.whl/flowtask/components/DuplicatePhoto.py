from typing import Callable, Dict, Any, Optional, List
import re
import asyncio
import asyncpg
from pgvector.asyncpg import register_vector
from navigator.libs.json import JSONContent
from .flow import FlowComponent
from ..exceptions import ConfigError, ComponentError
from ..conf import default_dsn

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def qid(name: str) -> str:
    """
    Very small helper to quote SQL identifiers safely.
    Raises if name contains anything but letters, digits or '_'.
    """
    if not IDENT_RE.match(name):
        raise ValueError(
            f"illegal identifier: {name!r}"
        )
    return '"' + name + '"'


class DuplicatePhoto(FlowComponent):
    """DuplicatePhoto.

    Check if Photo is Duplicated and add a column with the result.
    This component is used to check if a photo is duplicated in the dataset.
    It uses the image hash to check if the photo is duplicated.
    The image hash is a unique identifier for the image.
    The image hash is calculated using the image hash algorithm.
    The image hash algorithm is a fast and efficient way to calculate the hash of an image.
    saves a detailed information about matches based on perceptual hash and vector similarity.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.id_column: str = kwargs.get("id_column", "photo_id")
        self.hash_column: str = kwargs.get("hash_column", "image_hash")
        self.vector_column: str = kwargs.get("vector_column", "image_vector")
        self.hamming_threshold: int = kwargs.get("hamming_threshold", 4)
        self.vector_threshold: float = kwargs.get("vector_threshold", 0.05)
        self.tablename: str = kwargs.get("tablename", "image_bank")
        self.schema: str = kwargs.get("schema", "public")
        self.duplicate_column: str = kwargs.get("duplicate_column", "is_duplicated")
        self.pool: asyncpg.Pool | None = None
        super(DuplicatePhoto, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed

    def _qualified_tablename(self) -> str:
        """
        Get the qualified table name.
        """
        if not self.schema:
            raise ConfigError("Schema is not set.")
        if not self.tablename:
            raise ConfigError("Table name is not set.")
        return f"{qid(self.schema)}.{qid(self.tablename)}"

    def _build_phash_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) as distance "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3 "
            f"AND bit_count(('x' || $1)::bit(256) # ('x' || {qid(self.hash_column)})::bit(256)) <= $2 "
            f"ORDER BY distance ASC "
            f"LIMIT 1;"
        )

    def _build_vector_sql(self) -> str:
        return (
            f"SELECT {qid(self.id_column)}, "
            f"{qid(self.vector_column)} <-> $1::vector as distance "
            f"FROM {self._qualified_tablename()} "
            f"WHERE {qid(self.id_column)} IS DISTINCT FROM $3 "
            f"AND {qid(self.vector_column)} <-> $1::vector < $2 "
            f"ORDER BY distance ASC "
            f"LIMIT 1;"
        )

    async def pgvector_init(self, conn):
        """
        Initialize pgvector extension in PostgreSQL.
        """
        # Setup jsonb encoder/decoder
        def _encoder(value):
            # return json.dumps(value, cls=BaseEncoder)
            return self._encoder.dumps(value)  # pylint: disable=E1120

        def _decoder(value):
            return self._encoder.loads(value)  # pylint: disable=E1120

        await conn.set_type_codec(
            "json",
            encoder=_encoder,
            decoder=_decoder,
            schema="pg_catalog"
        )
        await conn.set_type_codec(
            "jsonb",
            encoder=_encoder,
            decoder=_decoder,
            schema="pg_catalog"
        )

        await register_vector(conn)

    # ──────────────────────────────────────────────────────────────
    # Setup / teardown
    # ──────────────────────────────────────────────────────────────
    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

        # column checks
        for col in (self.id_column, self.hash_column, self.vector_column,):
            if col not in self.data.columns:
                raise ConfigError(
                    f"Column '{col}' missing from DataFrame"
                )
        self.pool = await asyncpg.create_pool(
            dsn=default_dsn,
            min_size=1,
            max_size=4,
            max_queries=100,
            init=self.pgvector_init,
            timeout=10,
        )
        # Check if the table exists
        if not self.pool:
            raise ConfigError(
                "Database connection pool is not initialized."
            )
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    f"SELECT 1 FROM {self.schema}.{self.tablename} LIMIT 1"
                )
            except asyncpg.exceptions.UndefinedTableError:
                raise ConfigError(
                    f"Table {self.schema}.{self.tablename} does not exist."
                )
            except asyncpg.exceptions.UndefinedSchemaError:
                raise ConfigError(
                    f"Schema {self.schema} does not exist."
                )
        if self.duplicate_column not in self.data.columns:
            self.data[self.duplicate_column] = {
                "phash": None,
                "vector": None,
                "duplicate": False
            }
        # prepare SQL strings
        self._sql_phash = self._build_phash_sql()
        self._sql_vector = self._build_vector_sql()

    async def close(self):
        if self.pool:
            await self.pool.close()

    # --------------- duplicate test --------------------
    async def _check_duplicates(self, conn, phash: str, vec: list[float], current_id: int) -> Dict[str, Any]:
        """
        Check if the given hash and vector are duplicated in the database.
        Return detailed information about matches.

        :param conn: Database connection.
        :param phash: Perceptual hash of the image.
        :param vec: Vector representation of the image.
        :param current_id: Current photo ID.
        :return: Dictionary with detailed match information.
        """
        result = {
            "phash": None,
            "vector": None,
            "duplicate": False
        }

        # Check perceptual hash match
        if phash:
            phash_match = await conn.fetchrow(self._sql_phash, phash, self.hamming_threshold, current_id)
            if phash_match:
                result["phash"] = {
                    "duplicate": True,
                    self.id_column: phash_match[self.id_column],
                    "threshold": int(phash_match["distance"])
                }

        # Check vector match
        vector_match = await conn.fetchrow(self._sql_vector, vec, self.vector_threshold, current_id)
        if vector_match:
            # Ensure we have a valid distance value (must be positive and < threshold)
            distance = float(vector_match["distance"])
            if 0 <= distance < self.vector_threshold:
                result["vector"] = {
                    "duplicate": True,
                    "photo_id": vector_match[self.id_column],
                    "threshold": distance
                }

        # Determine overall duplicate status
        phash_duplicate = result["phash"] is not None and result["phash"]["duplicate"]
        vector_duplicate = result["vector"] is not None and result["vector"]["duplicate"]

        if phash_duplicate and vector_duplicate:
            result["duplicate"] = True
        elif not phash_duplicate and not vector_duplicate:
            # Both are false, duplicate remains None
            pass
        else:
            # Only one is true, duplicate is False
            result["duplicate"] = False

        return result

    async def _process_row(self, conn, row) -> Dict[str, Any]:
        """
        Process a row and check for duplicates with detailed information.

        :param conn: Database connection.
        :param row: Row data to process.
        :return: Dictionary with detailed match information.
        """
        phash = row[self.hash_column]
        vec = row[self.vector_column]
        current_id = row[self.id_column]

        # Log current processing information for debugging
        self._logger.debug(f"Processing photo_id: {current_id} with threshold: {self.vector_threshold}")

        duplicate_info = await self._check_duplicates(conn, phash, vec, current_id)

        # Debug information about match results
        if duplicate_info["vector"]:
            self._logger.debug(f"Vector match found: {duplicate_info['vector']}")
        if duplicate_info["phash"]:
            self._logger.debug(f"Perceptual hash match found: {duplicate_info['phash']}")

        # Update the row with duplicate information
        row[self.duplicate_column] = duplicate_info
        # if duplicate_info.get('duplicate', False) is True:
        #     row['is_duplicated'] = True
        return row

    async def run(self):
        """
        Run the duplicate detection with enhanced information.
        """
        if self.pool is None:
            raise ConfigError("Database connection pool is not initialized.")

        # Process rows and check for duplicates
        async def handle(idx):
            async with self._semaphore, self.pool.acquire() as conn:
                row = self.data.loc[idx].to_dict()
                updated_row = await self._process_row(conn, row)
                # Write duplicate info back into DataFrame
                return idx, updated_row[self.duplicate_column]

        results = await asyncio.gather(*(handle(i) for i in self.data.index))
        # Apply results to DataFrame all at once
        for idx, result in results:
            self.data.at[idx, self.duplicate_column] = result

        self._result = self.data
        return self._result
