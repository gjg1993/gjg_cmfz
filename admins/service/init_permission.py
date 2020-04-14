def init_permission(user, request):
    # 用户存在代表登录成功，则获取当前登录用户的权限

    permission_url = user.roles.filter(permissions__isnull=False).values("permissions__url",
                                                                         "permissions__is_menu",
                                                                         "permissions__title",
                                                                         "permissions__id",
                                                                         'permissions__menu_id',
                                                                         'permissions__html').distinct()

    # 用户可以访问的所用的权限
    # permission_list = [item['permissions__url'] for item in permission_url]

    # 用户权限中能够成为菜单的
    menu_list = []
    permission_list = []

    for url in permission_url:
        permission_list.append(url['permissions__url'])
        # 判断哪些是菜单的url  True是菜单
        if url['permissions__is_menu']:
            temp = {
                "title": url['permissions__title'],
                "url": url['permissions__url'],
                "id": url['permissions__id'],
                'menu_id':url['permissions__menu_id'],
                'html':url['permissions__html']
            }
            menu_list.append(temp)
    print("menu_list:", menu_list)
    # 将权限列表存入session
    request.session['permission_list'] = permission_list
    # 将菜单权限列表存入session
    request.session['menu_list'] = menu_list
