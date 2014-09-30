
######################
saga.adaptor.shell_job
######################

Description
-----------
 
The Shell job adaptor. This adaptor uses the sh command line tools (sh,
ssh, gsissh) to run local and remote jobs.  The adaptor expects the
login shell on the target host to be POSIX compliant.  However, one can
also specify a custom POSIX shell via the resource manager URL, like::

  js = saga.job.Service ("ssh://remote.host.net/bin/sh")

Note that custom shells in many cases will find a different environment
than the users default login shell!


Known Limitations:
******************

  * number of system pty's are limited:  each job.service object bound
    to this adaptor will use 2 pairs of pty pipes.  Systems usually
    limit the number of available pty's to 1024 .. 4096.  Given that
    other process also use pty's , that gives a hard limit to the number
    of object instances which can be created concurrently.  Hitting the
    pty limit will cause the following error message (or similar)::

      NoSuccess: pty_allocation or process creation failed (ENOENT: no more ptys)

    This limitation comes from saga.utils.pty_process.  On Linux
    systems, the utilization of pty's can be monitored::

       echo "allocated pty's: `cat /proc/sys/kernel/pty/nr`"
       echo "available pty's: `cat /proc/sys/kernel/pty/max`"


  * number of ssh connections are limited: sshd's default configuration,
    which is in place on many systems, limits the number of concurrent
    ssh connections to 10 per user -- beyond that, connections are
    refused with the following error::

      NoSuccess: ssh_exchange_identification: Connection closed by remote host

    As the communication with the ssh channel is unbuffered, the
    dropping of the connection will likely cause this error message to
    be lost.  Instead, the adaptor will just see that the ssh connection
    disappeared, and will issue an error message similar to this one::

      NoSuccess: read from pty process failed (Could not read line - pty process died)

 
  * number of processes are limited: the creation of an job.service
    object will create one additional process on the local system, and
    two processes on the remote system (ssh daemon clone and a shell
    instance).  Each remote job will create three additional processes:
    two for the job instance itself (double fork), and an additional
    process which monitors the job for state changes etc.  Additional
    temporary processes may be needed as well.  

    While marked as 'obsolete' by POSIX, the `ulimit` command is
    available on many systems, and reports the number of processes
    available per user (`ulimit -u`)

    On hitting process limits, the job creation will fail with an error
    similar to either of these::
    
      NoSuccess: failed to run job (/bin/sh: fork: retry: Resource temporarily unavailable)
      NoSuccess: failed to run job -- backend error

  * number of files are limited, as is disk space: the job.service will
    
    keep job state on the remote disk, in ``~/.saga/adaptors/shell_job/``.
    Quota limitations may limit the number of files created there,
    and/or the total size of that directory.  

    On quota or disk space limits, you may see error messages similar to
    the following ones::
    
      NoSuccess: read from pty process failed ([Errno 5] Quota exceeded)
      NoSuccess: read from pty process failed ([Errno 5] Input/output error)
      NoSuccess: find from pty process [Thread-5] failed (Could not read - pty process died)
      


  * Other system limits (memory, CPU, selinux, accounting etc.) apply as
    usual.

  
  * thread safety: it is safe to create multiple :class:`job.Service`
    instances to the same target host at a time -- they should not
    interfere with each other, but ``list()`` will list jobs created by
    either instance (if those use the same target host user account).

    It is **not** safe to use the *same* :class:`job.Service` instance
    from multiple threads concurrently -- the communication on the I/O
    channel will likely get screwed up.  This limitation may be removed
    in future versions of the adaptor.  Non-concurrent (i.e. serialized)
    use should work as expected though.





Supported Schemas
-----------------

This adaptor is triggered by the following URL schemes:

======================== ============================================================
schema                   description                                                 
======================== ============================================================
**ssh://**               use ssh to run remote jobs                                  
**fork://**              use /bin/sh to run jobs                                     
**local://**             alias for fork://                                           
**gsissh://**            use gsissh to run remote jobs                               
======================== ============================================================



Example
-------

.. literalinclude:: ../../../examples/jobs/localjob.py


Configuration Options
---------------------
Configuration options can be used to control the adaptor's     runtime behavior. Most adaptors don't need any configuration options     to be set in order to work. They are mostly for controlling experimental     features and properties of the adaptors.

     .. seealso:: More information about configuration options can be found in     the :ref:`conf_file` section.

enabled
*******

enable / disable saga.adaptor.shell_job adaptor

  - **type** : <type 'bool'>
  - **default** : True
  - **environment** : None
  - **valid options** : [True, False]

enable_notifications
********************

Enable support for job state notifications.  Note that
enabling this option will create a local thread, a remote 
shell process, and an additional network connection.
In particular for ssh/gsissh where the number of
concurrent connections is limited to 10, this
effectively halfs the number of available job service
instances per remote host.


  - **type** : <type 'bool'>
  - **default** : False
  - **environment** : None
  - **valid options** : [True, False]

purge_on_start
**************

Purge job information (state, stdio, ...) for all
jobs which are in final state when starting the job
service instance.  Note that this will purge *all*
suitable jobs, including the ones managed by another,
live job service instance.


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
                         :ref:`security_contexts` : userpass username/password pair for ssh
                              :ref:`security_contexts` : ssh public/private keypair
============================================================ ============================================================

Supported Job Description Attributes
************************************

  - Executable
  - Arguments
  - Environment
  - WorkingDirectory
  - Input
  - Output
  - Error
  - WallTimeLimit
  - TotalCPUCount
  - SPMDVariation



Supported API Classes
---------------------

This adaptor supports the following API classes:
  - :class:`saga.job.Service`
  - :class:`saga.job.Job`

Method implementation details are listed below.

saga.job.Service
****************

.. autoclass:: saga.adaptors.shell.shell_job.ShellJobService
   :members:


saga.job.Job
************

.. autoclass:: saga.adaptors.shell.shell_job.ShellJob
   :members:



