from setuptools import setup, find_packages
from setuptools.command.install import install

# 自定义安装命令，根据 extras_require 动态调整包包含规则
class CustomInstall(install):
    def run(self):
        # 检查是否启用了 "all" 选项
        if "all" in self.distribution.extras_require:
            # 覆盖 packages 参数，包含所有包（不再排除 tools）
            self.distribution.packages = find_packages()
        super().run()

exclude_packages=[
    "wxw.tools", "wxw.tools.*",
    "wxw.scripts", "wxw.scripts.*"
]

setup(
    name='wxw',
    version='1.0.7',
    keywords=['pip', 'wxw'],
    description='A library for wxw',
    long_description="Includes some ways to work with pictures, add qt utils",
    author='weixianwei',
    author_email='weixianwei0129@gmail.com',
    url='https://github.com/weixianwei0129/wxwLibrary',
    
    # 默认安装时排除 wxw.tools
    packages=find_packages(exclude=exclude_packages),
    platforms="any",
    install_requires=["numpy<2.0.0", "psutil", "opencv-python", "matplotlib", "Pillow", "einops", "PyYaml"],
    
    # 定义 "all" 选项（无需额外依赖，仅触发逻辑）
    extras_require={
        "all": []
    },
    
    # 注册自定义安装命令
    cmdclass={
        "install": CustomInstall
    }
)