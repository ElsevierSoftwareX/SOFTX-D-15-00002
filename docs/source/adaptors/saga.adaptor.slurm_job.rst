
######################
saga.adaptor.slurm_job
######################

Description
-----------
 
The SLURM adaptor allows to run and manage jobs on a 
`SLURM <https://computing.llnl.gov/linux/slurm/slurm.html>`_ HPC cluster.

Implementation Notes
********************

 - If scontrol can't find an exit code, it returns None
   (see _job_get_exit_code)
 - If scancel can't cancel a job, we raise an exception
   (see _job_cancel)
 - If we can't suspend a job with scontrol suspend, we raise an exception
   (see _job_suspend).  scontrol suspend NOT supported on Stampede
 - I started to implement a dictionary to keep track of jobs locally.
   It works to the point where the unit tests are passed, but I have
   not gone over theis extensively...
 - Relating to the above, _job_get_info is written, but unused/untested
   (mostly from PBS adaptor)





Supported Schemas
-----------------

This adaptor is triggered by the following URL schemes:

======================== ============================================================
schema                   description                                                 
======================== ============================================================
**slurm://**             connect to a local cluster                                  
**slurm+ssh://**         conenct to a remote cluster via SSH                         
**slurm+gsissh://**      connect to a remote cluster via GSISSH                      
======================== ============================================================



Example
-------

.. literalinclude:: ../../../examples/jobs/slurmjob.py


Configuration Options
---------------------
Configuration options can be used to control the adaptor's     runtime behavior. Most adaptors don't need any configuration options     to be set in order to work. They are mostly for controlling experimental     features and properties of the adaptors.

     .. seealso:: More information about configuration options can be found in     the :ref:`conf_file` section.

enabled
*******

enable / disable saga.adaptor.slurm_job adaptor

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
                             :ref:`security_contexts` : x509 X509 proxy for gsissh
                         :ref:`security_contexts` : userpass username/password pair for simple ssh
                              :ref:`security_contexts` : ssh public/private keypair
============================================================ ============================================================

Supported Job Description Attributes
************************************

  - Name
  - Executable
  - Arguments
  - Environment
  - SPMDVariation
  - TotalCPUCount
  - NumberOfProcesses
  - ProcessesPerHost
  - ThreadsPerProcess
  - WorkingDirectory
  - Input
  - Output
  - Error
  - FileTransfer
  - Cleanup
  - JobStartTime
  - WallTimeLimit
  - TotalPhysicalMemory
  - Queue
  - Project
  - JobContact



Supported API Classes
---------------------

This adaptor supports the following API classes:
  - :class:`saga.job.Service`
  - :class:`saga.job.Job`

Method implementation details are listed below.

saga.job.Service
****************

.. autoclass:: saga.adaptors.slurm.slurm_job.SLURMJobService
   :members:


saga.job.Job
************

.. autoclass:: saga.adaptors.slurm.slurm_job.SLURMJob
   :members:



