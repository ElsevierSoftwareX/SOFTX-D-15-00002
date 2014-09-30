
###########################
saga.adaptor.shell_resource
###########################

Description
-----------
 
The Shell resource adaptor. This adaptor attempts to determine what job
submission endpoint and file system resources are available for a given
host, and provides the respective access URLs.




Supported Schemas
-----------------

This adaptor is triggered by the following URL schemes:

======================== ============================================================
schema                   description                                                 
======================== ============================================================
**shell://**             find access URLs for shell-job/file adaptors                
======================== ============================================================



Example
-------

.. literalinclude:: ../../../examples/jobs/localresource.py


Configuration Options
---------------------
Configuration options can be used to control the adaptor's     runtime behavior. Most adaptors don't need any configuration options     to be set in order to work. They are mostly for controlling experimental     features and properties of the adaptors.

     .. seealso:: More information about configuration options can be found in     the :ref:`conf_file` section.

enabled
*******

enable / disable saga.adaptor.shell_resource adaptor

  - **type** : <type 'bool'>
  - **default** : True
  - **environment** : None
  - **valid options** : [True, False]



Capabilities
------------

Supported Monitorable Metrics
*****************************

  - State
  - StateDetail

Supported Context Types
***********************

============================================================ ============================================================
                                                   Attribute Description
============================================================ ============================================================
                             :ref:`security_contexts` : x509 X509 proxy for gsissh
                         :ref:`security_contexts` : userpass username/password pair for ssh
                              :ref:`security_contexts` : ssh public/private keypair
============================================================ ============================================================

res_attributes
**************

  - Rtype
  - MachineOS
  - MachineArch
  - Size
  - Memory
  - Access

rdes_attributes
***************

  - Rtype
  - MachineOS
  - MachineArch
  - Size
  - Memory
  - Access



Supported API Classes
---------------------

This adaptor supports the following API classes:
  - :class:`saga.resource.Manager`
  - :class:`saga.resource.Compute`

Method implementation details are listed below.

saga.resource.Manager
*********************

.. autoclass:: saga.adaptors.shell.shell_resource.ShellResourceManager
   :members:


saga.resource.Compute
*********************

.. autoclass:: saga.adaptors.shell.shell_resource.ShellResourceCompute
   :members:



