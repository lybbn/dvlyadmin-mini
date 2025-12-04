import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from mysystem.models import Dept, Button, Menu, MenuButton, Role, Users,Notification,NotificationUsers,SystemConfig,Dictionary


class Initialize:
    def __init__(self, delete=False):
        """
        :param delete: 是否删除已初始化数据
        """
        self.delete = delete
        self.creator_id = "0"

    def save(self, obj, data: list, name):
        """通用保存方法"""
        print(f"正在初始化【{name}】")
        
        if self.delete:
            try:
                obj.objects.filter(id__in=[ele.get('id') for ele in data if ele.get('id')]).delete()
            except Exception as e:
                print(f"删除{name}数据时出错: {str(e)}")

        for ele in data:
            m2m_dict = {}
            new_data = {}
            
            for key, value in ele.items():
                if isinstance(value, list):
                    m2m_dict[key] = value
                else:
                    new_data[key] = value

            try:
                object, created = obj.objects.update_or_create(
                    id=ele.get("id"), 
                    defaults=new_data
                )
                
                for key, m2m in m2m_dict.items():
                    m2m = list(set(m2m))
                    if m2m and m2m[0]:
                        m2m_field = getattr(object, key)
                        m2m_field.set(m2m)
                        
            except Exception as e:
                print(f"保存{name}数据时出错(ID:{ele.get('id')}): {str(e)}")

        print(f"初始化完成【{name}】")

    def init_dept(self):
        """
        初始化部门信息
        python .\manage.py  get_init_data mysystem.Dept
        """
        self.dept_data = [
            {"id": "8b304f92647747aabffc7e8750397762", "name": "lyadmin团队","key":"lyadmin", "sort": 1, "parent_id": None},
            {"id": "5e5af490ab0146d09045e6ece736c05f", "name": "财务部门","key":"caiwu", "sort": 2,"parent_id": "8b304f92647747aabffc7e8750397762"},
            {"id": "877641076a3b4a93b2e58e02246dbf3e", "name": "研发部门","key":"yanfa", "sort": 3,"parent_id": "8b304f92647747aabffc7e8750397762"},
        ]
        self.save(Dept, self.dept_data, "部门信息")

    def init_button(self):
        """初始化权限表标识"""
        self.button_data = [
            {"id": "1", "name": "编辑", "value": "Update"},
            {"id": "2", "name": "删除", "value": "Delete"},
            {"id": "3", "name": "详情", "value": "Detail"},
            {"id": "4", "name": "新增", "value": "Create"},
            {"id": "5", "name": "查询", "value": "Search"},
            {"id": "6", "name": "保存", "value": "Save"},
            {"id": "7", "name": "导出", "value": "Export"},
            {"id": "8", "name": "导入", "value": "Import"},
            {"id": "9", "name": "重置密码", "value": "ResetPass"},
            {"id": "10", "name": "修改密码", "value": "ChangePass"},
            {"id": "11", "name": "禁用", "value": "Disable"},
            {"id": "12", "name": "日志", "value": "Logs"},
            {"id": "13", "name": "移动", "value": "Move"},
            {"id": "14", "name": "设置状态", "value": "SetStatus"},
        ]
        self.save(Button, self.button_data, "权限表标识")

    def init_menu(self):
        """
        初始化菜单表
        python .\manage.py  get_init_data mysystem.Menu
        """
        self.menu_data = [
            {'id': '01599f73f61848aa811f687b1cfc1588', 'creator_id': '0', 'parent_id': None, 'icon': 'Football', 'name': '功能演示', 'sort': 60, 'type': 0, 'link_url': '', 'web_path': '/functionsDemosDirs', 'component': '', 'component_name': '', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '150e0957200146b3bd0226c45e8031f7', 'creator_id': '0', 'parent_id': '01599f73f61848aa811f687b1cfc1588', 'icon': 'Link', 'name': 'iframe嵌套', 'sort': 61, 'type': 2, 'link_url': 'https://doc.lybbn.cn', 'web_path': '/docdvlyadmin', 'component': '', 'component_name': '', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '1b5018bdb5e04698b84da505e8a6b93c', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'TrophyBase', 'name': '角色管理', 'sort': 100, 'type': 1, 'link_url': '', 'web_path': '/roleManage', 'component': 'system/role/roleManage', 'component_name': 'roleManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '205910763e0e42fbbc12833d2f7d61bb', 'creator_id': '0', 'parent_id': '563092a536194a1493551a0043f1f1a3', 'icon': 'Reading', 'name': '字典管理', 'sort': 30, 'type': 1, 'link_url': '', 'web_path': '/sysDictionary', 'component': 'system/dict/sysDictionary', 'component_name': 'sysDictionary', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '24d2eb79a21141afbe73058cc02545e0', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'ChatLineSquare', 'name': '操作日志', 'sort': 200, 'type': 1, 'link_url': '', 'web_path': '/journalManage', 'component': 'system/log/journalManage', 'component_name': 'journalManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '2e9937b37ac94e248e9ed159bfe7b655', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'Collection', 'name': '菜单管理', 'sort': 90, 'type': 1, 'link_url': '', 'web_path': '/menuManage', 'component': 'system/menu/menuManage', 'component_name': 'menuManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '31552696153b42599ce1faf6fe495824', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'User', 'name': '用户管理', 'sort': 40, 'type': 1, 'link_url': '', 'web_path': '/buserManage', 'component': 'system/user/buserManage', 'component_name': 'buserManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '44662b7fe6b54395994f28ed88eaf3f0', 'creator_id': '0', 'parent_id': None, 'icon': 'Message', 'name': '我的消息', 'sort': 30, 'type': 1, 'link_url': '', 'web_path': '/myMessage', 'component': 'system/messageCenter/myMessage', 'component_name': 'myMessage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '4a7a7748387f44dbab72027d8bdc87f7', 'creator_id': '0', 'parent_id': None, 'icon': 'House', 'name': '首页', 'sort': 10, 'type': 1, 'link_url': '', 'web_path': '/home', 'component': 'system/home/home', 'component_name': 'home', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '4f947108c5bf44f2b97e4a80daebf772', 'creator_id': '0', 'parent_id': '563092a536194a1493551a0043f1f1a3', 'icon': 'ChatDotRound', 'name': '通知公告', 'sort': 20, 'type': 1, 'link_url': '', 'web_path': '/messagNotice', 'component': 'system/messageCenter/messagNotice', 'component_name': 'messagNotice', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '563092a536194a1493551a0043f1f1a3', 'creator_id': '0', 'parent_id': None, 'icon': 'Operation', 'name': '系统工具', 'sort': 80, 'type': 0, 'link_url': '', 'web_path': '/systemToolsMgDirs', 'component': '', 'component_name': '', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '6354ba32ae734b5eaa799a65f76deee6', 'creator_id': '0', 'parent_id': '563092a536194a1493551a0043f1f1a3', 'icon': 'Setting', 'name': '系统设置', 'sort': 27, 'type': 1, 'link_url': '', 'web_path': '/systemConfig', 'component': 'system/config/systemConfig', 'component_name': 'systemConfig', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '8faec98030e443b99ce0d4c636163db7', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'Guide', 'name': '权限管理', 'sort': 120, 'type': 1, 'link_url': '', 'web_path': '/authorityManage', 'component': 'system/role/authorityManage', 'component_name': 'authorityManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '95227fe101e747908c12b56d2bae5e8e', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'OfficeBuilding', 'name': '部门管理', 'sort': 50, 'type': 1, 'link_url': '', 'web_path': '/deptManage', 'component': 'system/dept/deptManage', 'component_name': 'deptManage', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '98870fbaffb348ab9fd16a88e946bf09', 'creator_id': '0', 'parent_id': None, 'icon': 'User', 'name': '个人中心', 'sort': 19, 'type': 1, 'link_url': '', 'web_path': '/PersonalCenter', 'component': 'system/usercenter/PersonalCenter', 'component_name': 'PersonalCenter', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': '9ece0330c65e40df8da00190107d908e', 'creator_id': '0', 'parent_id': '01599f73f61848aa811f687b1cfc1588', 'icon': 'Link', 'name': '外链测试', 'sort': 60, 'type': 3, 'link_url': 'https://doc.lybbn.cn', 'web_path': '/docdvlyadminlink', 'component': '', 'component_name': '', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': 'a8b435647f0b4a3f852ec796433e8919', 'creator_id': '0', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'icon': 'AddLocation', 'name': '登录日志', 'sort': 230, 'type': 1, 'link_url': '', 'web_path': '/loginLogs', 'component': 'system/log/loginLogs', 'component_name': 'loginLogs', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
            {'id': 'af862854dc44410d84b8b2ae5c16c90d', 'creator_id': '0', 'parent_id': None, 'icon': 'Setting', 'name': '系统管理', 'sort': 90, 'type': 0, 'link_url': '', 'web_path': '/dirsettingsDirs', 'component': '', 'component_name': '', 'status': True, 'isautopm': False, 'cache': False, 'visible': True},
        ]
        self.save(Menu, self.menu_data, "菜单表")

    def init_menu_button(self):
        """
        初始化菜单权限表
        python .\manage.py  get_init_data mysystem.MenuButton
        """
        self.menu_button_data = [
            {'id': 1, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '查询', 'value': 'menuManage:Search', 'api': '/api/system/menu/', 'method': 0},
            {'id': 2, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '新增', 'value': 'deptManage:Create', 'api': '/api/system/dept/', 'method': 1},
            {'id': 3, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '删除', 'value': 'deptManage:Delete', 'api': '/api/system/dept/{id}/', 'method': 3},
            {'id': 4, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '编辑', 'value': 'deptManage:Update', 'api': '/api/system/dept/{id}/', 'method': 2},
            {'id': 5, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '查询', 'value': 'deptManage:Search', 'api': '/api/system/dept/', 'method': 0},
            {'id': 7, 'menu_id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '新增', 'value': 'roleManage:Create', 'api': '/api/system/role/', 'method': 1},
            {'id': 8, 'menu_id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '删除', 'value': 'roleManage:Delete', 'api': '/api/system/role/{id}/', 'method': 3},
            {'id': 9, 'menu_id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '编辑', 'value': 'roleManage:Update', 'api': '/api/system/role/{id}/', 'method': 2},
            {'id': 10, 'menu_id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '查询', 'value': 'roleManage:Search', 'api': '/api/system/role/', 'method': 0},
            {'id': 12, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '删除', 'value': 'menuManage:Delete', 'api': '/api/system/menu/{id}/', 'method': 3},
            {'id': 13, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '新增', 'value': 'menuManage:Create', 'api': '/api/system/menu/', 'method': 1},
            {'id': 14, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '编辑', 'value': 'menuManage:Update', 'api': '/api/system/menu/{id}/', 'method': 2},
            {'id': 15, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '移动', 'value': 'menuManage:Move', 'api': '/api/system/menu/update_sort/', 'method': 1},
            {'id': 16, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '导出', 'value': 'deptManage:Export', 'api': '/api/system/dept/export_data/', 'method': 1},
            {'id': 17, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '设置状态', 'value': 'deptManage:SetStatus', 'api': '/api/system/dept/set_status/', 'method': 1},
            {'id': 18, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '导入', 'value': 'deptManage:Import', 'api': '/api/system/dept/import_data/', 'method': 1},
            {'id': 19, 'menu_id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '设置状态', 'value': 'roleManage:SetStatus', 'api': '/api/system/role/set_status/', 'method': 1},
            {'id': 20, 'menu_id': '8faec98030e443b99ce0d4c636163db7', 'name': '查询', 'value': 'authorityManage:Search', 'api': '/api/system/role_permission/', 'method': 0},
            {'id': 21, 'menu_id': '8faec98030e443b99ce0d4c636163db7', 'name': '保存', 'value': 'authorityManage:Save', 'api': '/api/system/role_permission/save_permission/', 'method': 1},
            {'id': 22, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '新增', 'value': 'buserManage:Create', 'api': '/api/system/user/', 'method': 1},
            {'id': 23, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '删除', 'value': 'buserManage:Delete', 'api': '/api/system/user/{id}/', 'method': 3},
            {'id': 24, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '编辑', 'value': 'buserManage:Update', 'api': '/api/system/user/{id}/', 'method': 2},
            {'id': 25, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '查询', 'value': 'buserManage:Search', 'api': '/api/system/user/', 'method': 0},
            {'id': 27, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '导出', 'value': 'buserManage:Export', 'api': '/api/system/user/export_data/', 'method': 1},
            {'id': 28, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '导入', 'value': 'buserManage:Import', 'api': '/api/system/user/import_data/', 'method': 1},
            {'id': 29, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '设置状态', 'value': 'buserManage:SetStatus', 'api': '/api/system/user/set_status/', 'method': 1},
            {'id': 30, 'menu_id': '31552696153b42599ce1faf6fe495824', 'name': '重置密码', 'value': 'buserManage:ResetPass', 'api': '/api/system/user/reset_password/', 'method': 2},
            {'id': 31, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮查看', 'value': 'menuManage:ButtonSearch', 'api': '/api/system/button/', 'method': 0},
            {'id': 32, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮增', 'value': 'menuManage:ButtonCreate', 'api': '/api/system/button/', 'method': 1},
            {'id': 33, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮改', 'value': 'menuManage:ButtonUpdate', 'api': '/api/system/button/{id}/', 'method': 2},
            {'id': 34, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮删', 'value': 'menuManage:ButtonDelete', 'api': '/api/system/button/{id}/', 'method': 3},
            {'id': 35, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮权查', 'value': 'menuManage:MenuButtonSearch', 'api': '/api/system/menu_button/', 'method': 0},
            {'id': 36, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮权增', 'value': 'menuManage:MenuButtonCreate', 'api': '/api/system/menu_button/', 'method': 1},
            {'id': 37, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮权改', 'value': 'menuManage:MenuButtonUpdate', 'api': '/api/system/menu_button/{id}/', 'method': 2},
            {'id': 38, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮权删', 'value': 'menuManage:MenuButtonDelete', 'api': '/api/system/menu_button/{id}/', 'method': 3},
            {'id': 39, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '列权查看', 'value': 'menuManage:MenuFieldSearch', 'api': '/api/system/menu_field/', 'method': 0},
            {'id': 40, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '列权新增', 'value': 'menuManage:MenuFieldCreate', 'api': '/api/system/menu_field/', 'method': 1},
            {'id': 41, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '列权编辑', 'value': 'menuManage:MenuFieldUpdate', 'api': '/api/system/menu_field/{id}/', 'method': 2},
            {'id': 42, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '列权删除', 'value': 'menuManage:MenuFieldDelete', 'api': '/api/system/menu_field/{id}/', 'method': 3},
            {'id': 43, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '列权批量', 'value': 'menuManage:MenuFieldPL', 'api': '/api/system/menu_field/auto_create/', 'method': 1},
            {'id': 44, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '按钮权批', 'value': 'menuManage:MenuButtonPL', 'api': '/api/system/menu_button/auto_create/', 'method': 1},
            {'id': 45, 'menu_id': '8faec98030e443b99ce0d4c636163db7', 'name': '菜单', 'value': 'authorityManage:MenuSearch', 'api': '/api/system/role_id_to_menu/{id}/', 'method': 0},
            {'id': 47, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '查询', 'value': 'PersonalCenter:Search', 'api': '/api/system/user/user_info/', 'method': 0},
            {'id': 48, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '重置密码', 'value': 'PersonalCenter:ResetPass', 'api': '/api/system/user/change_password/', 'method': 1},
            {'id': 49, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '编辑', 'value': 'PersonalCenter:Update', 'api': '/api/system/user/user_info/', 'method': 2},
            {'id': 50, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '修改头像', 'value': 'PersonalCenter:UpdateAvatar', 'api': '/api/system/user/change_avatar/', 'method': 1},
            {'id': 51, 'menu_id': '24d2eb79a21141afbe73058cc02545e0', 'name': '查询', 'value': 'journalManage:Search', 'api': '/api/system/operation_log/', 'method': 0},
            {'id': 52, 'menu_id': '24d2eb79a21141afbe73058cc02545e0', 'name': '删除', 'value': 'journalManage:Delete', 'api': '/api/system/operation_log/{id}/', 'method': 3},
            {'id': 53, 'menu_id': '24d2eb79a21141afbe73058cc02545e0', 'name': '全部清除', 'value': 'journalManage:DeleteAll', 'api': '/api/system/operation_log/deletealllogs/', 'method': 3},
            {'id': 54, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '日志查询', 'value': 'PersonalCenter:GetOPLog', 'api': '/api/system/operation_log/getOwnerLogs/', 'method': 0},
            {'id': 55, 'menu_id': '205910763e0e42fbbc12833d2f7d61bb', 'name': '查询', 'value': 'sysDictionary:Search', 'api': '/api/system/dictionary/', 'method': 0},
            {'id': 56, 'menu_id': '205910763e0e42fbbc12833d2f7d61bb', 'name': '新增', 'value': 'sysDictionary:Create', 'api': '/api/system/dictionary/', 'method': 1},
            {'id': 57, 'menu_id': '205910763e0e42fbbc12833d2f7d61bb', 'name': '删除', 'value': 'sysDictionary:Delete', 'api': '/api/system/dictionary/{id}/', 'method': 3},
            {'id': 58, 'menu_id': '205910763e0e42fbbc12833d2f7d61bb', 'name': '编辑', 'value': 'sysDictionary:Update', 'api': '/api/system/dictionary/{id}/', 'method': 2},
            {'id': 59, 'menu_id': '205910763e0e42fbbc12833d2f7d61bb', 'name': '设置状态', 'value': 'sysDictionary:SetStatus', 'api': '/api/system/dictionary/set_status/', 'method': 1},
            {'id': 60, 'menu_id': 'a8b435647f0b4a3f852ec796433e8919', 'name': '查询', 'value': 'loginLogs:Search', 'api': '/api/system/login_log/', 'method': 0},
            {'id': 61, 'menu_id': 'a8b435647f0b4a3f852ec796433e8919', 'name': '删除', 'value': 'loginLogs:Delete', 'api': '/api/system/login_log/{id}/', 'method': 3},
            {'id': 62, 'menu_id': 'a8b435647f0b4a3f852ec796433e8919', 'name': '全部清除', 'value': 'loginLogs:DeleteAll', 'api': '/api/system/login_log/deletealllogs/', 'method': 3},
            {'id': 63, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '登录日志', 'value': 'PersonalCenter:GetLoginLog', 'api': '/api/system/login_log/getOwnerLogs/', 'method': 0},
            {'id': 64, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '新增分组', 'value': 'systemConfig:CreateGroup', 'api': '/api/system/sysconfig/', 'method': 1},
            {'id': 65, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '新增项', 'value': 'systemConfig:CreateContent', 'api': '/api/system/sysconfig/', 'method': 1},
            {'id': 66, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '保存', 'value': 'systemConfig:Save', 'api': '/api/system/sysconfig/{id}/', 'method': 2},
            {'id': 67, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '查询', 'value': 'systemConfig:Search', 'api': '/api/system/sysconfig/', 'method': 0},
            {'id': 68, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '删除', 'value': 'systemConfig:Delete', 'api': '/api/system/sysconfig/{id}/', 'method': 3},
            {'id': 69, 'menu_id': '6354ba32ae734b5eaa799a65f76deee6', 'name': '编辑', 'value': 'systemConfig:Update', 'api': '/api/system/sysconfig/{id}/', 'method': 2},
            {'id': 70, 'menu_id': '4f947108c5bf44f2b97e4a80daebf772', 'name': '查询', 'value': 'messagNotice:Search', 'api': '/api/system/msg/', 'method': 0},
            {'id': 71, 'menu_id': '4f947108c5bf44f2b97e4a80daebf772', 'name': '新增', 'value': 'messagNotice:Create', 'api': '/api/system/msg/', 'method': 1},
            {'id': 72, 'menu_id': '4f947108c5bf44f2b97e4a80daebf772', 'name': '删除', 'value': 'messagNotice:Delete', 'api': '/api/system/msg/{id}/', 'method': 3},
            {'id': 73, 'menu_id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '消息查询', 'value': 'PersonalCenter:PMsg', 'api': '/api/system/msg/ownmsg/', 'method': 0},
            {'id': 74, 'menu_id': '4f947108c5bf44f2b97e4a80daebf772', 'name': '编辑', 'value': 'messagNotice:Update', 'api': '/api/system/msg/{id}/', 'method': 2},
            {'id': 75, 'menu_id': '44662b7fe6b54395994f28ed88eaf3f0', 'name': '查询', 'value': 'myMessage:Search', 'api': '/api/system/msg/ownmsg/', 'method': 0},
            {'id': 76, 'menu_id': '44662b7fe6b54395994f28ed88eaf3f0', 'name': '删除', 'value': 'myMessage:Delete', 'api': '/api/system/msg/delownmsg/', 'method': 1},
            {'id': 77, 'menu_id': '44662b7fe6b54395994f28ed88eaf3f0', 'name': '详情', 'value': 'myMessage:Detail', 'api': '/api/system/msg/readownmsg/', 'method': 1},
        ]
        self.save(MenuButton, self.menu_button_data, "菜单权限表")

    def init_role(self):
        """初始化角色表"""
        data = [
            {"id": "854f77a5df34497a9af1d16379821f2b", "name": "管理员", "key": "admin", "sort": 1, "status": 1},
        ]
        self.save(Role, data, "角色表")

    def init_users(self):
        """初始化用户表"""
        data = [
            {
                "id": "0",
                "password": "pbkdf2_sha256$260000$oE0tnjC7PRIV6aCEah0J1F$scZo6l2/kekoClW8jZ6bM4PmSXevb4qzqHLro8PvzLc=",
                "is_superuser": 1, "is_staff": 1, "identity": 0,
                "is_active": 1, "username": "superadmin", "name": "超级管理员", "nickname": "超级管理员",
                "dept_id": "",
            },
            {
                "id": "1792aea416944eff9e3845aec6ac88b4",
                "password": "pbkdf2_sha256$260000$DO6dpT8e4Ls0yD51grncC8$KZfswxNJ8MILTWwy+bicRyU7Q3PKC4orn4SJbhIkN4Q=",
                "is_superuser": 0, "is_staff": 1, "identity": 1,"gender":2,
                "is_active": 1, "username": "admin", "name": "管理员", "nickname": "管理员",
                "dept_id": "8b304f92647747aabffc7e8750397762",
                "role": ["854f77a5df34497a9af1d16379821f2b"],
            },
            {
                "id": "2",
                "password": "pbkdf2_sha256$260000$oivECWOjB0GJyMjPsrqb3t$9FvnYtXtsNWDva2P3A/eIg6cRMLOp7kiIOuwfLKyDAY=",
                "is_superuser": 0, "is_staff": 0, "identity": 2,
                "is_active": 1, "username": "test", "name": "前端用户", "mobile": "18888888888", "nickname": "前端用户",
                "dept_id": "",
                "role": [],
            },
        ]
        self.save(Users, data, "用户表")
    
    def init_notification(self):
        """
        初始化消息表
        python .\manage.py  get_init_data mysystem.Notification
        """
        data = [
            {'id': '52c13c36bdda427ab72020fa8e0db443', 'creator_id': '0', 'title': 'dvlyadmin-mini版本发布通知', 'content': '<p><span style="color: rgb(86, 156, 214); font-size: 14px;">dvlyadmin-mini</span><span style="color: rgb(0, 0, 0); font-size: 14px;">是专为追求页面极致效果的开发者设计的一套 </span><span style="color: rgb(86, 156, 214); font-size: 14px;">django-vue-lyadmin优化升级</span><span style="color: rgb(204, 204, 204); font-size: 14px;"> </span><span style="color: rgb(0, 0, 0); font-size: 14px;">的精简版。我们通过大量重构架构，去除了无用冗余代码，力求做到小而 精。前端采用</span><span style="color: rgb(204, 204, 204); font-size: 14px;"> </span><span style="color: rgb(86, 156, 214); font-size: 14px;">**Vite + Vue 3 + Element Plus**</span><span style="color: rgb(0, 0, 0); font-size: 14px;">，支持适配手机端，助力快速开发项目及提升项目质量！</span></p>', 'target_type': 0, 'tag_type': 0}
        ]
        self.save(Notification, data, "消息表")

    def init_notification_users(self):
        """
        初始化消息用户表
        python .\manage.py  get_init_data mysystem.NotificationUsers
        """
        data = [
            {'id': 1, 'user_id': '1792aea416944eff9e3845aec6ac88b4', 'notification_id': '52c13c36bdda427ab72020fa8e0db443', 'is_read': False, 'read_at': None},
            {'id': 2, 'user_id': '0', 'notification_id': '52c13c36bdda427ab72020fa8e0db443', 'is_read': False, 'read_at': None},
        ]
        self.save(NotificationUsers, data, "消息用户表")
    
    def init_systemconfig(self):
        """
        初始化系统配置表
        python .\manage.py  get_init_data mysystem.SystemConfig
        """
        data = [
            {'id': '11da46ef4d494aa0be2ff5958ff98f0b', 'creator_id': '0', 'parent_id': '3593fb777e1e4f77a1e62ed7eb0681a7', 'title': '登录验证码', 'key': 'loginCaptcha', 'value': 'true', 'sort': 8, 'status': True, 'data_options': None, 'form_item_type': 9, 'rule': None, 'placeholder': None, 'tip': '登录验证码开启/关闭', 'setting': None},
            {'id': '3593fb777e1e4f77a1e62ed7eb0681a7', 'creator_id': '0', 'parent_id': None, 'title': '基础配置', 'key': 'base', 'value': None, 'sort': 0, 'status': True, 'data_options': None, 'form_item_type': 0, 'rule': None, 'placeholder': None, 'tip': None, 'setting': None},
            {'id': '59421c76edb34bc8a7ba622cb6ed8133', 'creator_id': '0', 'parent_id': '3593fb777e1e4f77a1e62ed7eb0681a7', 'title': 'logo', 'key': 'logo', 'value': 'http://127.0.0.1:8000/media/platform/2025-07-08/20250708113144_688.png', 'sort': 10, 'status': True, 'data_options': None, 'form_item_type': 7, 'rule': None, 'placeholder': None, 'tip': None, 'setting': None},
            {'id': '5d66345539d849e4b4ad766e99c0b25f', 'creator_id': '0', 'parent_id': None, 'title': 'Api白名单', 'key': 'apiWhiteList', 'value': '[]', 'sort': 0, 'status': True, 'data_options': None, 'form_item_type': 0, 'rule': None, 'placeholder': None, 'tip': None, 'setting': None},
            {'id': '8b9a6e5f079e4fbe8627185c2322d9b0', 'creator_id': '0', 'parent_id': '3593fb777e1e4f77a1e62ed7eb0681a7', 'title': '系统标题', 'key': 'systitle', 'value': 'dvlyadmin-mini', 'sort': 5, 'status': True, 'data_options': None, 'form_item_type': 0, 'rule': None, 'placeholder': '请输入系统标题', 'tip': None, 'setting': None},
        ]
        self.save(SystemConfig, data, "系统配置表")
    
    def init_dictionary(self):
        """
        初始化字典管理
        python .\manage.py  get_init_data mysystem.Dictionary
        """
        data = [
            {'id': '1b999b8fd390470bb39e57b134f841f5', 'creator_id': '0', 'label': '是', 'value': 'true', 'status': True, 'sort': 1, 'parent_id': '526c712ec30e45a2a1b45174e98420a3', 'remark': ''},
            {'id': '23724e0d5c14458e839efc01449ee1b0', 'creator_id': '0', 'label': '否', 'value': 'false', 'status': True, 'sort': 2, 'parent_id': '526c712ec30e45a2a1b45174e98420a3', 'remark': ''},
            {'id': '526c712ec30e45a2a1b45174e98420a3', 'creator_id': '0', 'label': '是/否-布尔值', 'value': 'button_bool', 'status': True, 'sort': 29, 'parent_id': None, 'remark': ''},
            {'id': '53623bd2de60426281fd490ef65be9ca', 'creator_id': '0', 'label': '女', 'value': '1', 'status': True, 'sort': 2, 'parent_id': 'e19dbebf1e3a49688e62cbc3f42486bc', 'remark': ''},
            {'id': '6d12f0aa25e14ccbb806b148f215a370', 'creator_id': '0', 'label': '是/否-数字值', 'value': 'button_number', 'status': True, 'sort': 30, 'parent_id': None, 'remark': ''},
            {'id': '85e5a570019742c58dc0a31f95aca8c0', 'creator_id': '0', 'label': '未知', 'value': '0', 'status': True, 'sort': 1, 'parent_id': 'e19dbebf1e3a49688e62cbc3f42486bc', 'remark': ''},    
            {'id': '97ddad1d630647f3b95616453dd55958', 'creator_id': '0', 'label': '男', 'value': '2', 'status': True, 'sort': 3, 'parent_id': 'e19dbebf1e3a49688e62cbc3f42486bc', 'remark': ''},
            {'id': 'a0b67efa43c54b8eabf5042988a887c4', 'creator_id': '0', 'label': '否', 'value': '0', 'status': True, 'sort': 2, 'parent_id': '6d12f0aa25e14ccbb806b148f215a370', 'remark': ''},
            {'id': 'ceb419b24926454681c9040389deda5d', 'creator_id': '0', 'label': '是', 'value': '1', 'status': True, 'sort': 1, 'parent_id': '6d12f0aa25e14ccbb806b148f215a370', 'remark': ''},
            {'id': 'e19dbebf1e3a49688e62cbc3f42486bc', 'creator_id': '0', 'label': '性别', 'value': 'gender', 'status': True, 'sort': 1, 'parent_id': None, 'remark': ''},
        ]
        self.save(Dictionary, data, "字典管理表")

    def run(self):
        """执行初始化"""
        try:
            self.init_dept()
            self.init_button()
            self.init_menu()
            self.init_menu_button()
            self.init_role()
            self.init_users()
            self.init_notification()
            self.init_notification_users()
            self.init_systemconfig()
            self.init_dictionary()
            print("所有初始化完成!")
        except Exception as e:
            print(f"初始化过程中出错: {str(e)}")


def main(is_delete=False):
    """主函数"""
    Initialize(is_delete).run()


if __name__ == '__main__':
    main()