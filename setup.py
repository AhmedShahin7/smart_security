from setuptools import find_packages, setup

package_name = 'smart_security'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmedmohamedmc55@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_stream = smart_security.camera_stream:main',
            'depth_estimation = smart_security.depth_estimation:main',
            'event_logger = smart_security.event_logger:main',
            'event_manager = smart_security.event_manager:main',
            'object_detection = smart_security.object_detection:main',
            'scene_analysis = smart_security.scene_analysis:main',
            'security_response = smart_security.security_response:main',  
            'system_monitor = smart_security.system_monitor:main',
            'alarm_controller = smart_security.alarm_controller:main'         
        ],
    },
)
