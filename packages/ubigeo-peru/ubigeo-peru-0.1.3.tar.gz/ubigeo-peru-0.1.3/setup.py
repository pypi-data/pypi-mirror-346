from setuptools import setup, find_packages

setup(
    name="ubigeo-peru",                          
    version="0.1.3",                              
    author="Elmer Yujra Condori",                           
    author_email="elmerjk.20@gmail.com",          
    description="Paquete para acceder a datos de UBIGEO de Perú",  
    long_description=open('README.md').read(),   
    long_description_content_type="text/markdown",  
    url="https://github.com/tuusuario/ubigeo-peru", 
    packages=find_packages(),                    
    classifiers=[                                 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[                                                          
        
    ],
    python_requires='>=3.6',                      
)