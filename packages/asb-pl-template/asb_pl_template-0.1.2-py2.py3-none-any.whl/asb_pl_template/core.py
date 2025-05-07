# asb-pl-template/core.py
# !/usr/bin/env python
# -*- coding:utf8 -*-
import os
import shutil
import time
from .constants import PROJECT_TEMPLATE, ROLE_TEMPLATE, SIMPLE_PLAYBOOK_TEMPLATE
from .logger import logger
from .lib import check_directory_exists


class AnsibleProjectManager:
    def __init__(self, project_name, roles_path=None, role_name=None, playbook_name=None):
        self.project_name = project_name
        self.roles_path = roles_path
        self.role_name = role_name
        self.playbook_name = playbook_name
        self.project_path = os.path.join(os.getcwd(), project_name)

    def create_directory_structure(self, path, template, project_name=None):
        """
        创建目录结构
        """
        for key, value in template.items():
            try:
                if isinstance(value, dict):
                    new_path = os.path.join(path, key)
                    if not check_directory_exists(new_path):
                        os.makedirs(new_path, exist_ok=True)
                        logger.debug(f"Created directory: {new_path}")
                    self.create_directory_structure(new_path, value, project_name)
                else:
                    file_path = os.path.join(path, key)
                    if project_name:
                        content = value.format(project_name=project_name)
                    else:
                        content = value
                    with open(file_path, 'w') as f:
                        f.write(content)
                    logger.debug(f"Created file: {file_path}")
            except Exception as e:
                logger.error(f"Error creating {key}: {e}")

    def create_project(self):
        """
        创建项目
        """
        try:
            logger.debug(f"Creating project: {self.project_name}")
            os.makedirs(self.project_path, exist_ok=True)

            # 创建项目结构
            self.create_directory_structure(self.project_path, PROJECT_TEMPLATE, self.project_name)

            if self.roles_path and self.role_name:
                # 确保角色目录创建在项目的 roles 目录下
                roles_full_path = os.path.join(self.project_path, 'roles')
                os.makedirs(roles_full_path, exist_ok=True)
                logger.debug(f"Created roles directory: {roles_full_path}")
                if isinstance(self.role_name, list):
                    for role in self.role_name:
                        role_path = os.path.join(roles_full_path, role)
                        os.makedirs(role_path, exist_ok=True)
                        self.create_directory_structure(role_path, ROLE_TEMPLATE)
                        logger.debug(f"Creating role: {role} in {roles_full_path}")
                else:
                    role_path = os.path.join(roles_full_path, self.role_name)
                    os.makedirs(role_path, exist_ok=True)
                    self.create_directory_structure(role_path, ROLE_TEMPLATE)
                    logger.debug(f"Creating role: {self.role_name} in {roles_full_path}")

            if self.playbook_name:
                playbook_path = os.path.join(self.project_path, 'playbooks', self.playbook_name)
                if self.playbook_name == 'simple_playbook.yml':
                    with open(playbook_path, 'w') as f:
                        f.write(SIMPLE_PLAYBOOK_TEMPLATE)
                else:
                    with open(playbook_path, 'w') as f:
                        f.write(f'# {self.playbook_name} playbook')
                logger.debug(f"Creating playbook: {self.playbook_name}")
        except Exception as e:
            logger.error(f"Error creating project: {e}")

    def backup(self, path):
        """
        备份指定路径的内容
        """
        backup_dir = os.path.join(os.getcwd(), 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"{os.path.basename(path)}-{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)
        try:
            shutil.copytree(path, backup_path)
            logger.info(f"Backed up {path} to {backup_path}")
        except Exception as e:
            logger.error(f"Error backing up {path}: {e}")

    def log_file_info(self, path):
        """
        记录文件或目录的详细信息
        """
        if os.path.isfile(path):
            size = os.path.getsize(path)
            created_time = time.ctime(os.path.getctime(path))
            logger.info(f"File: {path}, Size: {size} bytes, Created: {created_time}")
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    created_time = time.ctime(os.path.getctime(file_path))
                    logger.info(f"File: {file_path}, Size: {size} bytes, Created: {created_time}")

    def delete_project(self):
        """
        删除项目
        """
        if self.roles_path and self.role_name:
            target_path = os.path.join(self.project_path, 'roles', self.role_name)
            target_type = "role"
        else:
            target_path = self.project_path
            target_type = "project"

        if os.path.exists(target_path):
            confirm = input(f"Are you sure you want to delete this {target_type}: {target_path}? (y/n) ")
            if confirm.lower() == 'y':
                self.log_file_info(target_path)
                self.backup(target_path)
                try:
                    shutil.rmtree(target_path)
                    logger.info(f"Deleted {target_type}: {target_path}")
                except Exception as e:
                    logger.error(f"Error deleting {target_type}: {e}")
            else:
                logger.info(f"Deletion of {target_type} {target_path} cancelled.")
        else:
            logger.warning(f"{target_type.capitalize()} {target_path} does not exist.")
