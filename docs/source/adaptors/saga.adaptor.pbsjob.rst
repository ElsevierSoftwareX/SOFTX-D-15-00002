
###################
saga.adaptor.pbsjob
###################

Description
-----------

The PBS adaptor allows to run and manage jobs on `PBS <http://www.pbsworks.com/>`_
and `TORQUE <http://www.adaptivecomputing.com/products/open-source/torque>`_
controlled HPC clusters.



Supported Schemas
-----------------

This adaptor is triggered by the following URL schemes:

======================== ============================================================
schema                   description                                                 
======================== ============================================================
**pbs://**               connect to a local cluster                                  
**pbs+ssh://**           conenct to a remote cluster via SSH                         
**pbs+gsissh://**        connect to a remote cluster via GSISSH                      
======================== ============================================================



Example
-------

.. literalinclude:: ../../../examples/jobs/pbsjob.py


Configuration Options
---------------------
Configuration options can be used to control the adaptor's     runtime behavior. Most adaptors don't need any configuration options     to be set in order to work. They are mostly for controlling experimental     features and properties of the adaptors.

     .. seealso:: More information about configuration options can be found in     the :ref:`conf_file` section.

enabled
*******

enable / disable saga.adaptor.pbsjob adaptor

  - **type** : <type 'bool'>
  - **default** : True
  - **environment** : None
  - **valid options** : [True, False]



Capabilities
------------

Supported Monitorable Metrics
*****************************

  - State

Supported Job Attributes
************************

  - ExitCode
  - ExecutionHosts
  - Created
  - Started
  - Finished

Supported Context Types
***********************

============================================================ ============================================================
                                                   Attribute Description
============================================================ ============================================================
                             :ref:`security_contexts` : x509 GSISSH X509 proxy context
                         :ref:`security_contexts` : userpass username/password pair (ssh)
                              :ref:`security_contexts` : ssh SSH public/private keypair
============================================================ ============================================================

Supported Job Description Attributes
************************************

  - Name
  - Executable
  - Arguments
  - Environment
  - Input
  - Output
  - Error
  - Queue
  - Project
  - WallTimeLimit
  - WorkingDirectory
  - WallTimeLimit
  - SPMDVariation
  - TotalCPUCount

callbacks
*********

  - State



Supported API Classes
---------------------

This adaptor supports the following API classes:
  - :class:`saga.job.Service`
  - :class:`saga.job.Job`

Method implementation details are listed below.

saga.job.Service
****************

.. autoclass:: saga.adaptors.pbs.pbsjob.PBSJobService
   :members:


saga.job.Job
************

.. autoclass:: saga.adaptors.pbs.pbsjob.PBSJob
   :members:



