2. Edit the ``/etc/damera/damera.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://damera:DAMERA_DBPASS@controller/damera
