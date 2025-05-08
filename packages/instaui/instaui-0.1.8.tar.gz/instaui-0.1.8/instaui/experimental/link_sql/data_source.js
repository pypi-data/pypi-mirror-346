
export default {
    props: [],

    setup(props, { emit, expose }) {
        const filters = new Map()

        function addFilter(filter) {
            const { field, expr, value, replace = true, query_id } = filter
            const key = `${field}-${query_id}`

            if (!filters.has(key)) {
                filters.set(key, [])
            }

            const info = { expr, value }

            if (replace) {
                filters.set(key, [info])
            } else {
                filters.get(key).push(info)
            }
            emit("filter-changed", { filters: Object.fromEntries(filters.entries()), target: field, query_id })
        }

        function removeFilter(info) {
            const { field, query_id } = info
            const key = `${field}-${query_id}`

            filters.delete(key)
            emit("filter-changed", { filters: Object.fromEntries(filters.entries()), target: field, query_id })
        }



        function test(count) {
            console.log('test', count)
        }

        expose({
            test,
            addFilter,
            removeFilter,
        })


    },


}