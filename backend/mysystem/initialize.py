import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from mysystem.models import Dept, Button, Menu, MenuButton, Role, Users


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
        """初始化部门信息"""
        self.dept_data = [
            {"id": "cae96ade-7483-4827-bb0d-d2bd63ec1cc4", "name": "财务部门", "sort": 1,
             "parent_id": "d2c03bd9-dad0-4262-88ca-c3681d224fc3"},
            {"id": "d2c03bd9-dad0-4262-88ca-c3681d224fc3", "name": "lyadmin团队", "sort": 1, "parent_id": None},
            {"id": "fd8230ca-67bd-4347-8a9b-57eb19be5d9e", "name": "研发部门", "sort": 2,
             "parent_id": "d2c03bd9-dad0-4262-88ca-c3681d224fc3"},
        ]
        self.save(Dept, self.dept_data, "部门信息")

    def init_button(self):
        """初始化权限表标识"""
        self.button_data = [
            {"id": "4547b93a-36b9-410d-987c-3c52a9b51156", "name": "编辑", "value": "Update"},
            {"id": "4a410769-6b0a-4ed3-90f0-b5d89a6f802c", "name": "删除", "value": "Delete"},
            {"id": "644e9c34-e3d6-4518-b795-a603a6e9a137", "name": "详情", "value": "Detail"},
            {"id": "80cb145b-5035-4517-a28a-7d59426f73f8", "name": "新增", "value": "Create"},
            {"id": "ccc3f35f-c80c-4929-b8cc-67531698f397", "name": "查询", "value": "Search"},
            {"id": "83a9b774-4669-4d2f-b61d-8ee4944c2316", "name": "保存", "value": "Save"},
            {"id": "2d763a6d6dcf409d87056efd06aace0a", "name": "修改密码", "value": "ChangePass"},
            {"id": "6e0a41e5308c44a8b0d2785e05b2c07a", "name": "禁用", "value": "Disable"},
            {"id": "09134d7643504804a6c7cc3d16e06684", "name": "日志", "value": "Logs"}
        ]
        self.save(Button, self.button_data, "权限表标识")

    def init_menu(self):
        """初始化菜单表"""
        self.menu_data = [
            # 主菜单
            {'id': '9065cb5445ac42ef93eb9e75e6287792', 'name': 'DashBoard', 'sort': 1, 'web_path': 'analysis', 'icon': 'DataLine', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': '2e3438c8-3ddc-43ff-b8d8-cca328e4856e', 'name': '管理员管理', 'sort': 3, 'web_path': 'adminManage', 'icon': 'avatar', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': '244b28685cd14a39a383189981510d4a', 'name': '用户管理', 'sort': 5, 'web_path': 'userManage', 'icon': 'user-filled', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': 'd73f73a399af48cea6a8490ac508d7a0', 'name': '用户管理CRUD', 'sort': 7, 'web_path': 'userManageCrud', 'icon': 'user-filled', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': 'd4e2fe169a8b40f3846421ac04e4fccb', 'name': '平台设置', 'sort': 9, 'web_path': '', 'icon': 'platform', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'name': '系统管理', 'sort': 990, 'web_path': '', 'icon': 'tools', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': '25735adb-d051-4b7b-bbb7-1154526f3e4c', 'name': '个人中心', 'sort': 13, 'web_path': 'personalCenter', 'icon': 'user', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': 'c236fb6b-ddaa-4deb-b79b-16e42d9f347f', 'name': '日志管理', 'sort': 999, 'web_path': 'journalManage', 'icon': 'info-filled', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            {'id': '77edf447326b4e0dbc6f9719c1de8a12', 'name': '系统监控', 'sort': 888, 'web_path': '', 'icon': 'TrendCharts', 'parent_id': None, 'visible': 1, 'isautopm': 0},
            
            # 子菜单
            {'id': '4236eb70-1558-43a0-9cf2-037230c547f9', 'name': '部门管理', 'sort': 1, 'web_path': 'departmentManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'component': 'system/dept', 'component_name': 'dept', 'visible': 1, 'isautopm': 0},
            {'id': '56c3f341-4f46-4b04-9cfc-c8a14701707e', 'name': '菜单管理', 'sort': 2, 'web_path': 'menuManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'component': 'system/menu', 'component_name': 'menu', 'visible': 1, 'isautopm': 0},
            {'id': '15c9ebc5-d12f-470a-a560-938a7dc57570', 'name': '角色管理', 'sort': 3, 'web_path': 'roleManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'component': 'system/role', 'component_name': 'role', 'visible': 1, 'isautopm': 0},
            {'id': 'a607e820-36e5-45c0-aabf-85a8e4e2c7ac', 'name': '权限管理', 'sort': 4, 'web_path': 'authorityManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'component': 'system/rolePermission', 'component_name': 'rolePermission', 'visible': 1, 'isautopm': 0},
            {'id': '151035da-77a3-4a62-b474-fce6824571fb', 'name': '按钮管理', 'sort': 6, 'web_path': 'buttonManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'component': 'system/button', 'component_name': 'buttonManage', 'visible': 0, 'isautopm': 0},
            {'id': '02c24003527546359b5a77ae07adc7d5', 'name': '地区管理', 'sort': 7, 'web_path': 'areaManage', 'parent_id': '54f769b0-3dff-416c-8102-e55ec44827cc', 'visible': 1, 'isautopm': 0},
            
            # 其他子菜单...
        ]
        self.save(Menu, self.menu_data, "菜单表")

    def init_menu_button(self):
        """初始化菜单权限表"""
        self.menu_button_data = [
            # 示例数据
            {'id': 'e7fa30290d37447585ea7583d9d01f1b', 'menu_id': 'ae5629946df4497cbec10419e8375dd9', 'name': '编辑', 'value': 'Update', 'api': '/api/platformsettings/lunboimg/{id}/', 'method': 2},
            {'id': '6e4251a948f348ccaa419a777a118048', 'menu_id': '80a340eae92b430abe17635468c2df1d', 'name': '编辑', 'value': 'Update', 'api': '/api/platformsettings/other/{id}/', 'method': 2},
            {'id': '0209de89-6b9f-4d8a-84d3-ccfc3cc8b4da', 'menu_id': '151035da-77a3-4a62-b474-fce6824571fb', 'name': '编辑', 'value': 'Update', 'api': '/api/system/button/{id}/', 'method': 2},
            # 其他按钮权限...
        ]
        self.save(MenuButton, self.menu_button_data, "菜单权限表")

    def init_role(self):
        """初始化角色表"""
        data = [
            {"id": "36001d1a-1b3e-4413-bdfe-b3bc04375f46", "name": "管理员", "key": "admin", "sort": 1, "status": 1, "data_scope": 4},
            {"id": "35b58d98-b506-4f93-be79-ed1e109da071", "name": "普通用户", "key": "public", "sort": 2, "status": 1, "data_scope": 0}
        ]
        self.save(Role, data, "角色表")

    def init_users(self):
        """初始化用户表"""
        data = [
            {
                "id": "0",
                "password": "pbkdf2_sha256$260000$oE0tnjC7PRIV6aCEah0J1F$scZo6l2/kekoClW8jZ6bM4PmSXevb4qzqHLro8PvzLc=",
                "is_superuser": 1, "is_staff": 1, "identity": 0,
                "is_active": 1, "username": "superadmin", "name": "超级管理员",
                "dept_id": "d2c03bd9-dad0-4262-88ca-c3681d224fc3",
            },
            {
                "id": "d1431450-5068-4461-b57e-7862c005a547",
                "password": "pbkdf2_sha256$260000$DO6dpT8e4Ls0yD51grncC8$KZfswxNJ8MILTWwy+bicRyU7Q3PKC4orn4SJbhIkN4Q=",
                "is_superuser": 0, "is_staff": 1, "identity": 1,
                "is_active": 1, "username": "admin", "name": "管理员",
                "dept_id": "d2c03bd9-dad0-4262-88ca-c3681d224fc3",
                "role": ["36001d1a-1b3e-4413-bdfe-b3bc04375f46"],
            },
            {
                "id": "244b28685cd14a39a383189981510d4a",
                "password": "pbkdf2_sha256$260000$oivECWOjB0GJyMjPsrqb3t$9FvnYtXtsNWDva2P3A/eIg6cRMLOp7kiIOuwfLKyDAY=",
                "is_superuser": 0, "is_staff": 0, "identity": 2,
                "is_active": 1, "username": "test", "name": "测试用户", "mobile": "18888888888", "nickname": "测试用户",
                "dept_id": "",
                "role": [],
            },
        ]
        self.save(Users, data, "用户表")

    def run(self):
        """执行初始化"""
        try:
            self.init_dept()
            self.init_button()
            self.init_menu()
            self.init_menu_button()
            self.init_role()
            self.init_users()
            print("所有初始化完成!")
        except Exception as e:
            print(f"初始化过程中出错: {str(e)}")


def main(is_delete=False):
    """主函数"""
    Initialize(is_delete).run()


if __name__ == '__main__':
    main()