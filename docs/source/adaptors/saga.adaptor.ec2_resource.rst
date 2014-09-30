
#########################
saga.adaptor.ec2_resource
#########################

Description
-----------
 
The EC2 resource adaptor. This adaptor interacts with a variety of
IaaS backends via the Apache LibCloud.  It also provides EC2 related
context types.




Supported Schemas
-----------------

This adaptor is triggered by the following URL schemes:

======================== ============================================================
schema                   description                                                 
======================== ============================================================
**ec2://**               Amacon EC2 key/secret                                       
**ec2_keypair://**       Amacon EC2 keypair name                                     
======================== ============================================================



Example
-------

.. literalinclude:: ../../../examples/resource/amazon_ec2.py


Configuration Options
---------------------
Configuration options can be used to control the adaptor's     runtime behavior. Most adaptors don't need any configuration options     to be set in order to work. They are mostly for controlling experimental     features and properties of the adaptors.

     .. seealso:: More information about configuration options can be found in     the :ref:`conf_file` section.

enabled
*******

enable / disable saga.adaptor.ec2_resource adaptor

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
                      :ref:`security_contexts` : ec2_keypair ec2 keypair for node access
                              :ref:`security_contexts` : ec2 EC2 ID and Secret
============================================================ ============================================================

res_attributes
**************

  - Rtype
  - Template
  - Image
  - MachineOS
  - MachineArch
  - Size
  - Memory
  - Access

rdes_attributes
***************

  - Rtype
  - Template
  - Image
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

.. autoclass:: saga.adaptors.aws.ec2_resource.EC2ResourceManager
   :members:


saga.resource.Compute
*********************

.. autoclass:: saga.adaptors.aws.ec2_resource.EC2ResourceCompute
   :members:



