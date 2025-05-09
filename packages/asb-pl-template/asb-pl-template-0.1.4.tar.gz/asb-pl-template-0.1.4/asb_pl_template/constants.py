#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 定义banner
banner = r"""
           _                 _       _                       _       _
  __ _ ___| |__        _ __ | |     | |_ ___ _ __ ___  _ __ | | __ _| |_ ___
 / _` / __| '_ \ _____| '_ \| |_____| __/ _ \ '_ ` _ \| '_ \| |/ _` | __/ _ \
| (_| \__ \ |_) |_____| |_) | |_____| ||  __/ | | | | | |_) | | (_| | ||  __/
 \__,_|___/_.__/      | .__/|_|      \__\___|_| |_| |_| .__/|_|\__,_|\__\___|
                      |_|                             |_|
"""
# 定义项目结构模板
PROJECT_TEMPLATE = {
    '.asb-pl-template': {},
    'README.md': '# {project_name}\n\nThis is a description of the {project_name} project.',
    'ansible.cfg': '[defaults]\n# Add your ansible configuration here',
    'hosts': '# Add your production hosts here\n[prod]\n# Add your staging hosts here\n[stage]\n# Add your local hosts here\n[local]\nlocalhost ansible_connection=local',
    'group_vars': {
        'main.yml': '# Common variables for all environments',
        'local.yml': '# Variables for local development',
        'prod.yml': '# Variables for production environment',
        'stage.yml': '# Variables for staging environment'
    },
    'host_vars': {
        'prod.yml': '# Variables for production hosts',
        'stage.yml': '# Variables for staging hosts'
    },
    'library': {},
    'requirements.yml': '# List your role dependencies here',
    'playbooks': {
        'site.yml': '# Main playbook\n - hosts: all\n   roles:\n     - role: common\n     - role: web\n     - role: database',
        'site-local.yml': '# Playbook for local development\n - hosts: local\n   roles:\n     - role: common\n     - role: web\n     - role: database',
        'site-prod.yml': '# Playbook for production environment\n - hosts: prod\n   roles:\n     - role: common\n     - role: web\n     - role: database',
        'site-stage.yml': '# Playbook for staging environment\n - hosts: stage\n   roles:\n     - role: common\n     - role: web\n     - role: database'
    },
    'inventories': {
        'prod': {
            'group_vars': {},
            'host_vars': {},
            'inventory': '# Production inventory file'
        },
        'stage': {
            'group_vars': {},
            'host_vars': {},
            'inventory': '# Staging inventory file'
        }
    },
    'roles': {},
    'tests': {
        'test.yml': '# Playbook for testing \n ---\n - hosts: all\n   gather_facts: no\n   tasks:\n     - name: Test task\n       debug:\n         msg: "This is a test task"'
    }
}

# 定义角色结构模板
ROLE_TEMPLATE = {
    'tasks': {
        'main.yml': '---\n- name: Main tasks\n  debug:\n    msg: "This is the main task"\n  tags:\n    - always\n- name: Another task\n  debug:\n    msg: "This is another task"\n  tags:\n    - always',
    },
    'handlers': {
        'main.yml': '- name: Main handlers\n  debug:\n    msg: "This is the main handler"'
    },
    'templates': {
        'ntp.conf.j2': '# NTP configuration template'
    },
    'files': {
        'bar.txt': 'This is a sample text file',
        'foo.sh': '#!/bin/bash\n# This is a sample script'
    },
    'vars': {
        'main.yml': '# Variables for this role'
    },
    'defaults': {
        'main.yml': '# Default variables for this role'
    },
    'meta': {
        'main.yml': '# Role dependencies'
    }
}

# 新增简单的 playbook 模板
SIMPLE_PLAYBOOK_TEMPLATE = """
# 简单的 Ansible Playbook 示例
---
# 目标主机组
- hosts: all
  gather_facts: yes
  become: yes
  become_method: sudo

  # 任务列表
  tasks:
    - name: 显示主机名
      debug:
        msg: "当前主机名是 {{ ansible_hostname }}"

    - name: install packages
      apt: name=apt-transport-https,ca-certificates,curl,software-properties-common state=present

    - name: import key
      shell: curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

    - name: import installation source on ubuntu1804
      shell: add-apt-repository "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu {{ubuntu1804}} stable"
      when: ansible_facts['distribution_major_version'] == "18"

    - name: import installation source on ubuntu2004
      shell: add-apt-repository "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu {{ubuntu2004}} stable"
      when: ansible_facts['distribution_major_version'] == "20"

    - name: install docker for ubuntu1804
      apt: name=docker-ce={{docker_version}}{{ubuntu1804}},docker-ce-cli={{docker_version}}{{ubuntu1804}}
      when: ansible_facts['distribution_major_version'] == "18"

    - name: install docker for ubuntu2004
      apt: name=docker-ce={{docker_version}}{{ubuntu2004}},docker-ce-cli={{docker_version}}{{ubuntu2004}}
      when: ansible_facts['distribution_major_version'] == "20"

    - name: mkdir /etc/docker
      file: path=/etc/docker state=directory

    - name: aliyun Mirror acceleration
      copy: src=/data/ansible/files/daemon.json dest=/etc/docker/

    - name: load daemon
      shell: systemctl daemon-reload

    - name: start docker
      service: name=docker state=started enabled=yes
# ...
# 使用示例
# 假设该 playbook 文件名为 simple_playbook.yml
# 运行 playbook 到所有主机：
# ansible-playbook simple_playbook.yml -i hosts
# 运行 playbook 到特定主机组：
# ansible-playbook simple_playbook.yml -i hosts --limit group_name
"""

import os


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), "__init__.py")
version_line = list(filter(lambda l: l.startswith("VERSION"), open(init)))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))
