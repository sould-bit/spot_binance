# spot_binance

este codigo pretende , realizar test  de prueva  para crear logicas de bots , rentables  


# CONFIGURACION DEL ENTORNO

!pip install virtualenv  # debemos instalar ,  el entorno
!virtualenv bot_tradingenv # lo nombramos


!source /content/bot_tradingenv/bin/activate # lo activamos


# configuracion de TA-LIB ADICIONAL

# download TA-Lib
!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

!tar xvzf ta-lib-0.4.0-src.tar.gz


import os
os.chdir('ta-lib') # Can't use !cd in co-lab

!./configure --prefix=/usr

!make #El comando make install se utiliza para copiar el programa construido,
      # sus bibliotecas y documentación en las ubicaciones correctas. Por lo general,
      # se utiliza después de ejecutar el comando make, que compila el código fuente. En Google Colab,
      # puede usar !pip install o !apt-get install para importar una biblioteca que no está en Colaboratory por defecto.

!make install
# wait ~ 30s

!os.chdir('../')
!ls

!pip install TA-Lib

print("TA-LIB  HA SIDO INSTALADO")

