from pathlib import Path
from typing import Dict, TypeVar
import itertools
from instaui import ui, arco
from ._base import DataSourceElement
from ._types import TFilters, TQueryStrInfo

try:
    import pandas
    import duckdb
except ImportError as e:
    raise e


TElementClass = TypeVar("TElementClass", bound=ui.element)


class DuckdbDataFrameSource:
    QUERY_ID: int = 0

    def __init__(
        self,
        table_name: str,
    ):
        super().__init__()

        self._element = DataSourceElement()
        self._conn = duckdb.connect(":default:", read_only=False)
        self._table_name = table_name

    def _generate_query_id(self):
        self.QUERY_ID += 1
        return self.QUERY_ID

    def __getitem__(self, field: str):
        def use_fn(cls: type[TElementClass]) -> TElementClass:
            if issubclass(cls, arco.select):
                return self.__apply_select(field)(cls)

            if issubclass(cls, arco.input):
                return self.__apply_input(field)(cls)

            raise NotImplementedError(f"Not supported component:{cls.__name__}")

        return use_fn

    def __query_distinct_field_values(
        self, field: str, query_id: int, order_sql: str = ""
    ):
        @ui.computed(inputs=[self.__query_str_info(field, query_id), field, order_sql])
        def query_distinct_field_values_computed(
            with_filters_info: TQueryStrInfo, field: str, order_sql: str
        ):
            sql = f"with cte as ({with_filters_info['sql']}) select distinct {field} from cte {order_sql}"

            local_con = self._conn.cursor()

            query = local_con.sql(sql, params=with_filters_info["params"])
            return list(itertools.chain(*query.fetchall()))

        return query_distinct_field_values_computed

    def __apply_select(self, field: str):
        def use_fn(cls: type[arco.select]) -> arco.select:
            query_id = self._generate_query_id()
            element = cls(
                self.__query_distinct_field_values(
                    field=field, query_id=query_id, order_sql=f"order by {field}"
                )
            )

            on_change = ui.js_event(
                inputs=[ui.event_context.e(), field, query_id],
                outputs=[self._element._ele_ref],
                code=r"""(value,field,query_id) => {
if (value) {
    return {method: 'addFilter', args:[{field, expr: `${field}= ?`,value,query_id}]};
}

return {method:'removeFilter', args:[{field,query_id}]};
                }""",
            )

            element.on_change(on_change)

            return element

        return use_fn

    def __apply_input(self, field: str):
        def use_fn(cls: type[arco.input]) -> arco.input:
            query_id = self._generate_query_id()
            element = cls()

            on_change = ui.js_event(
                inputs=[ui.event_context.e(), field, query_id],
                outputs=[self._element._ele_ref],
                code=r"""(value,field,query_id) => {
if (value) {
    value = `%${value.trim()}%`
    return {method: 'addFilter', args:[{field, expr: `${field} like ?`,value,replace:true,query_id}]};
}

return {method:'removeFilter', args:[{field,query_id}]};
                }""",
            )

            element.on_input(on_change)

            return element

        return use_fn

    def __query_str_info(self, target_field: str = "", query_id: int = -1):
        @ui.computed(inputs=[self._element.filters, target_field, query_id])
        def query_str_computed(filters: TFilters, target_field: str, query_id: int):
            if not filters:
                return {
                    "sql": f"select * from {self._table_name}",
                    "params": [],
                }
            else:
                filter_exprs = []

                if target_field:
                    target_key = f"{target_field}-{query_id}"
                    without_target_exprs = (
                        exprs for key, exprs in filters.items() if key != target_key
                    )
                    filter_exprs = list(itertools.chain(*without_target_exprs))
                else:
                    filter_exprs = list(itertools.chain(*filters.values()))

                where_stem = " and ".join(info["expr"] for info in filter_exprs)
                if where_stem:
                    where_stem = f" where {where_stem}"
                return {
                    "sql": f"select * from {self._table_name}{where_stem}",
                    "params": [info["value"] for info in filter_exprs],
                }

        return query_str_computed

    def query_str(self):
        return ui.js_computed(
            inputs=[self.__query_str_info()],
            code=r"""info=>{
    const {sql,params} = info;
    let currentIndex = 0;
    return sql.replace(/\?/g, function () {
        if (currentIndex >= params.length) {
            throw new Error('Not enough parameters provided for the SQL statement.');
        }
        return JSON.stringify(params[currentIndex++]);
    });                                                
}""",
        )

    def filters(self):
        return self._element.filters

    def __apply_table(self, *, sql: str):
        def use_fn(cls: type[arco.table]) -> arco.table:
            @ui.computed(inputs=[self.__query_str_info(), sql])
            def table_query(with_filters_into: TQueryStrInfo, sql: str):
                sql = f"with cte as ({with_filters_into['sql']}) {sql}"

                local_con = self._conn.cursor()

                query = local_con.sql(sql, params=with_filters_into["params"])
                columns = query.columns
                values = query.fetchall()

                real_cols = [{"title": col, "dataIndex": col} for col in columns]

                real_values = [
                    {col: val for col, val in zip(columns, row)} for row in values
                ]

                return {
                    "columns": real_cols,
                    "data": real_values,
                }

            element = cls(
                data=ui.js_computed(inputs=[table_query], code=r"v=> v ? v.data : []"),
                columns=ui.js_computed(
                    inputs=[table_query], code=r"v=> v ? v.columns : []"
                ),
            )

            return element

        return use_fn

    def __call__(self, cls: type[arco.table], *, sql: str = "select * from cte"):
        return self.__apply_table(sql=sql)(cls)

    def query_table(self, *, sql: str):
        return self.__apply_table(sql=sql)


class Facade:
    def __call__(self, db: Path):
        self.db = db
        raise NotImplementedError()

    @classmethod
    def from_pandas(
        cls, dataframe: "pandas.DataFrame", *, table_name: str = "df"
    ) -> DuckdbDataFrameSource:
        ds = DuckdbDataFrameSource(table_name)

        cursor = ds._conn.cursor()
        cursor.execute(
            f"create table if not exists {table_name} as select * from dataframe"
        )
        return ds


_facade = Facade()
