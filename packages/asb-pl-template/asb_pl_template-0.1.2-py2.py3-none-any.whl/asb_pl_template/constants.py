#!/usr/bin/env python3
# -*- coding:utf8 -*-

# 定义项目结构模板
PROJECT_TEMPLATE = {
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

    - name: 创建一个目录
      file:
        path: /tmp/ansible_test_dir
        state: directory
        mode: '0755'
    
    - name: 创建一个文件
      file:
        path: /tmp/ansible_test_file
        state: touch
        mode: '0644'
            
    - name: 删除一个文件
      file:
        path: /tmp/ansible_test_file
        state: absent
    
    - name: 删除一个目录
      file:
        path: /tmp/ansible_test_dir
        state: absent
        recurse: yes
    
    - name: 复制文件
      copy:
        src: /path/to/source_file
        dest: /path/to/destination_file
        mode: '0644'

    - name: 复制目录
      copy:
        src: /path/to/source_dir
        dest: /path/to/destination_dir
        mode: '0755'
        recurse: yes

    - name: 安装 Nginx
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: 启动 Nginx 服务
      service:
        name: nginx
        state: started
        enabled: yes
      when: ansible_os_family == "Debian"

# ...
# 使用示例
# 假设该 playbook 文件名为 simple_playbook.yml
# 运行 playbook 到所有主机：
# ansible-playbook simple_playbook.yml -i hosts
# 运行 playbook 到特定主机组：
# ansible-playbook simple_playbook.yml -i hosts --limit group_name
"""