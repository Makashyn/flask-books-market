


def filters(request_args, Model):
    list_data = []
    for filter_keyword in request_args:
        filter_condition = ''
        if '__' in filter_keyword:
            filter_condition = filter_keyword.split('__')[1]
        else:
            filter_condition = filter_keyword
        queryset = []
        if filter_condition == Model.__name__.lower():
            queryset = Model.query.filter(Model.name.contains(request_args.get(filter_keyword)[1])).all()
        elif filter_condition == 'startswith':
            queryset = Model.query.filter(Model.name.startswith(request_args.get(filter_keyword)[1])).all()
        elif filter_condition == 'price_lt':
            queryset = Model.query.filter(Model.price < request_args.get(filter_keyword)).all()
        elif filter_condition == 'price_gt':
            queryset = Model.query.filter(Model.price > request_args.get(filter_keyword)).all()
        if queryset:
            list_data = create_books_list(queryset)[:]

        return list_data


def create_books_list(queryset):
    list_data = []
    for item in queryset:
        list_data.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price
        })
    return list_data