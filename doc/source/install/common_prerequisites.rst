Prerequisites
-------------

Before you install and configure the damera service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``damera`` database:

     .. code-block:: none

        CREATE DATABASE damera;

   * Grant proper access to the ``damera`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON damera.* TO 'damera'@'localhost' \
          IDENTIFIED BY 'DAMERA_DBPASS';
        GRANT ALL PRIVILEGES ON damera.* TO 'damera'@'%' \
          IDENTIFIED BY 'DAMERA_DBPASS';

     Replace ``DAMERA_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``damera`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt damera

   * Add the ``admin`` role to the ``damera`` user:

     .. code-block:: console

        $ openstack role add --project service --user damera admin

   * Create the damera service entities:

     .. code-block:: console

        $ openstack service create --name damera --description "damera" damera

#. Create the damera service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        damera public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        damera internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        damera admin http://controller:XXXX/vY/%\(tenant_id\)s
