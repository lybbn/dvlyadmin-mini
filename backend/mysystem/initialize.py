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
            {"id": "8b304f92647747aabffc7e8750397762", "name": "lyadmin团队", "sort": 1, "parent_id": None},
            {"id": "5e5af490ab0146d09045e6ece736c05f", "name": "财务部门", "sort": 2,"parent_id": "8b304f92647747aabffc7e8750397762"},
            {"id": "877641076a3b4a93b2e58e02246dbf3e", "name": "研发部门", "sort": 3,"parent_id": "8b304f92647747aabffc7e8750397762"},
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
            {"id": "9", "name": "修改密码", "value": "ChangePass"},
            {"id": "10", "name": "禁用", "value": "Disable"},
            {"id": "11", "name": "日志", "value": "Logs"},
            {"id": "12", "name": "移动", "value": "Move"},
            {"id": "13", "name": "设置状态", "value": "SetStatus"},
        ]
        self.save(Button, self.button_data, "权限表标识")

    def init_menu(self):
        """初始化菜单表"""
        self.menu_data = [
            {'id': '4a7a7748387f44dbab72027d8bdc87f7', 'name': '首页','icon': 'House', 'sort': 10, 'web_path': '/home', 'parent_id': None, 'component': None, 'component_name': 'home', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '98870fbaffb348ab9fd16a88e946bf09', 'name': '个人中心','icon': 'User', 'sort': 19, 'web_path': '/PersonalCenter', 'parent_id': None, 'component': None, 'component_name': 'PersonalCenter', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '0c66eff6687d4fea8955a420850159c1', 'name': '个人中心简版','icon': 'User', 'sort': 22, 'web_path': '/PersonalCenters', 'parent_id': None, 'component': None, 'component_name': 'PersonalCenters', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '150e0957200146b3bd0226c45e8031f7', 'name': 'iframe嵌套','icon': 'Link', 'sort': 33, 'web_path': '/docdvlyadmin','link_url': 'https://doc.lybbn.cn', 'parent_id': None, 'component': None, 'component_name': None, 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '9ece0330c65e40df8da00190107d908e', 'name': '外链测试','icon': 'Link', 'sort': 36, 'web_path': '/docdvlyadminlink','link_url': 'https://doc.lybbn.cn', 'parent_id': None, 'component': None, 'component_name': None, 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': 'af862854dc44410d84b8b2ae5c16c90d', 'name': '系统管理','icon': 'Setting', 'sort': 40, 'web_path': '/PersonalCenters', 'parent_id': None, 'component': None, 'component_name': None, 'visible': 1,'cache': 0, 'isautopm': 0,'type': 0},
            {'id': '95227fe101e747908c12b56d2bae5e8e', 'name': '部门管理','icon': 'OfficeBuilding', 'sort': 50, 'web_path': '/deptManage', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'component': None, 'component_name': 'deptManage', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '菜单管理','icon': 'Collection', 'sort': 90, 'web_path': '/menuManage', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'component': None, 'component_name': 'menuManage', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
            {'id': '1b5018bdb5e04698b84da505e8a6b93c', 'name': '角色管理','icon': 'TrophyBase', 'sort': 100, 'web_path': '/roleManage', 'parent_id': 'af862854dc44410d84b8b2ae5c16c90d', 'component': None, 'component_name': 'roleManage', 'visible': 1,'cache': 0, 'isautopm': 0,'type': 1},
        ]
        self.save(Menu, self.menu_data, "菜单表")

    def init_menu_button(self):
        """初始化菜单权限表"""
        self.menu_button_data = [
            {'id': 1, 'menu_id': '2e9937b37ac94e248e9ed159bfe7b655', 'name': '查询', 'value': 'menuManage:Search', 'api': '/api/system/menu/', 'method': 0},
            {'id': 2, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '新增', 'value': 'deptManage:Create', 'api': '/api/system/dept/', 'method': 1},
            {'id': 3, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '删除', 'value': 'deptManage:Delete', 'api': '/api/system/dept/{id}/', 'method': 3},
            {'id': 4, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '编辑', 'value': 'deptManage:Update', 'api': '/api/system/dept/{id}/', 'method': 2},
            {'id': 5, 'menu_id': '95227fe101e747908c12b56d2bae5e8e', 'name': '查询', 'value': 'deptManage:Update', 'api': '/api/system/dept/', 'method': 0},
        ]
        self.save(MenuButton, self.menu_button_data, "菜单权限表")

    def init_role(self):
        """初始化角色表"""
        data = [
            {"id": "1", "name": "管理员", "key": "admin", "sort": 1, "status": 1, "data_scope": 4},
            {"id": "2", "name": "普通用户", "key": "public", "sort": 2, "status": 1, "data_scope": 0}
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
                "id": "1",
                "password": "pbkdf2_sha256$260000$DO6dpT8e4Ls0yD51grncC8$KZfswxNJ8MILTWwy+bicRyU7Q3PKC4orn4SJbhIkN4Q=",
                "is_superuser": 0, "is_staff": 1, "identity": 1,
                "is_active": 1, "username": "admin", "name": "管理员", "nickname": "管理员",
                "dept_id": "2",
                "role": ["1"],
            },
            {
                "id": "2",
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