# asb_pl_template/tests/test_asb-pl-template.py
import unittest
from unittest.mock import patch, MagicMock
from asb_pl_template import AnsibleProjectManager
import os


class TestASBPLTemplate(unittest.TestCase):

    def setUp(self):
        self.project_name = "test_project"
        self.manager = AnsibleProjectManager(self.project_name)

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_create_project(self, mock_open, mock_makedirs):
        # 测试创建项目的功能
        self.manager.create_project()

        # 断言项目目录被创建
        mock_makedirs.assert_any_call(self.manager.project_path, exist_ok=True)

        # 可以添加更多断言来检查其他目录和文件是否被创建
        # 例如，检查 roles 目录是否被创建
        roles_path = os.path.join(self.manager.project_path, 'roles')
        mock_makedirs.assert_any_call(roles_path, exist_ok=True)

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    def test_delete_project(self, mock_rmtree, mock_exists):
        # 测试删除项目的功能
        confirm_input = 'y'
        with patch('builtins.input', return_value=confirm_input):
            self.manager.delete_project()

        # 断言项目目录被删除
        mock_rmtree.assert_called_with(self.manager.project_path)

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    def test_delete_role(self, mock_rmtree, mock_exists):
        # 测试删除角色的功能
        role_name = "test_role"
        manager = AnsibleProjectManager(self.project_name, roles_path='.', role_name=role_name)
        confirm_input = 'y'
        with patch('builtins.input', return_value=confirm_input):
            manager.delete_project()

        # 断言角色目录被删除
        role_path = os.path.join(manager.project_path, 'roles', role_name)
        mock_rmtree.assert_called_with(role_path)


if __name__ == "__main__":
    unittest.main()
