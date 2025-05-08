# ansible-playbook-template

## 简介
ansible-playbook-template是一个用于快速生成ansible playbook的工具。

该工具可以帮助您快速生成ansible playbook的项目结构，同时也可以帮助您快速生成ansible playbook的role结构。

支持如下功能：
- [x] 快速生成项目结构
- [x] 快速生成role结构,同 ansible-galaxy init 功能一致,支持生成多个role
- [x] 快速生成playbook结构
- [] 快速生成inventory结构
- [] 快速生成host_vars结构
....

## 快速开始
```bash
pip install asb-pl-template

#You can install  asb-pl-template directly using pipx:
pipx install "git+https://github.com/hujianli94/asb-pl-template.git"
```

## 使用
```bash
# 快速生成项目结构,支持绝对路径和相对路径
asb-pl-template init project .
asb-pl-template init project ./test_project
asb-pl-template init project . --roles-path=./roles --role-names=common1
asb-pl-template init project . --role-names=common1

# 快速生成role
## 在当前目录下生成role,role名称默认为role_example
asb-pl-template init role .
# 在指定目录下生成role,role名称为common
asb-pl-template init role ./test/roles/common

# 快速生成多个role
## 在当前目录下生成多个role
asb-pl-template init role common1 common2
## 在指定目录下生成多个role
asb-pl-template init role ./test/roles/commo1 ./test/roles/commo2

# 快速生成playbook
asb-pl-template init playbook
# 在指定目录下生成playbook
asb-pl-template init playbook --playbook_path=./test/ deploy.yml
# 快速生成包含使用示例的简单 playbook
asb-pl-template init playbook --example --playbook_path=./test/ deploy.yml

# 使用 --verbose 参数开启详细日志输出
asb-pl-template init <project_name> --verbose
asb-pl-template init <role_name> --verbose 



## 生成项目结构如下
<project_name>/
├── README.md            # 该专案的说明文件
├── ansible.cfg          # ansible config file
├── hosts                # inventory file for production servers
├── group_vars/
│   ├── main.yml         # 各环境共用的 vars
│   ├── local.yml        # 本机开发的 vars
│   ├── prod.yml         # 正式环境的 vars
│   └── stage.yml        # 测试环境的 vars
├── host_vars
│   ├── prod.yml         # 正式环境的主机 vars
│   └── stage.yml        # 测试环境的主机 vars
├── library/             # 自定义的模块
├── requirements.yml     # 依赖的 role
├── playbooks/
│   └── site.yml         # 主 playbook
│   └── site-local.yml   # 本机开发的 playbook
│   └── site-prod.yml    # 正式环境的 playbook
│   └── site-stage.yml   # 测试环境的 playbook
└── inventories/
    ├── prod/
    │   ├── group_vars/   # 组 vars
    │   ├── host_vars/    # 主机 vars
    │   └── inventory/    # 主机清单文件
    └── stage/
        ├── group_vars/   # 组 vars
        ├── host_vars/    #
        └── inventory/    #
└── roles/
    └── <role_name>/        # role name
        ├── tasks/        #
        │   └── main.yml  # main tasks file
        ├── handlers/     #
        │   └── main.yml  # handlers file
        ├── templates/    #
        │   └── ntp.conf.j2 # templates end in .j2
        ├── files/        #
        │   ├── bar.txt   # files
        │   └── foo.sh    # script files
        ├── vars/         #
        │   └── main.yml  # variables with this role
        ├── defaults/     #
        │   └── main.yml  # default variables
        └── meta/         #
            └── main.yml  # role dependencies
└── tests/
    └── test.yml        # playbook for testing
```
