# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, The SAGA Project"
__license__   = "MIT"

""" Local job adaptor implementation 
"""

import os, time, socket, signal, subprocess

from   saga.utils.singleton import Singleton
from   saga.engine.engine   import getEngine, ANY_ADAPTOR
from   saga.utils.job.jobid import JobId
from   saga.utils.which     import which

import saga.cpi.base
import saga.cpi.job

SYNC  = saga.cpi.base.sync
ASYNC = saga.cpi.base.async

###############################################################################
# Adaptor capabilites and documentaton.
#
# - name
# - description
# - detailed description
# - supported schemas (& what they do)
# - supported config options -- Configurable
# - supported job descrption attributes
# - supported metrics
# - supported contexts

_adaptor_name           = 'saga.adaptor.LocalJob'

_adaptor_options = [
    { 
    'category'      : _adaptor_name,
    'name'          : 'foo', 
    'type'          : str, 
    'default'       : 'bar', 
    'valid_options' : None,
    'documentation' : 'dummy config option for unit test.',
    'env_variable'  : None
    }
]

_adaptor_capabilities   = {
    'jd_attributes' : [saga.job.EXECUTABLE,
                       saga.job.ARGUMENTS,
                       saga.job.ENVIRONMENT,
                       saga.job.WORKING_DIRECTORY,
                       saga.job.INPUT,
                       saga.job.OUTPUT,
                       saga.job.ERROR,
                       saga.job.SPMD_VARIATION,
                       saga.job.NUMBER_OF_PROCESSES],
    'metrics'       : [saga.job.STATE],
    'contexts'      : {}  # {context type : how it is used}
}

_adaptor_doc    = {
    'name'          : _adaptor_name,
    'description'   : """ The local job adaptor. This adaptor uses subprocesses to run jobs on the local machine
                      """,
    'details'       : """ A more elaborate description....
                      """,
    'schemas'       : {'fork':'desc', 'local':'same as fork'},
    'cfg_options'   : _adaptor_options,
    'capabilites'   : _adaptor_capabilities,

                  }

_adaptor_info   = {
    'name'          : _adaptor_name,
    'cpis'          : [
        { 
        'type'      : 'saga.job.Service',
        'class'     : 'LocalJobService',
        'schemas'   : ['fork', 'local']
        }, 
        { 
        'type'      : 'saga.job.Job',
        'class'     : 'LocalJob',
        'schemas'   : ['fork', 'local']
        }
    ]
}


###############################################################################
# The adaptor class

class Adaptor (saga.cpi.base.AdaptorBase) :
    ''' 
    This is the actual adaptor class, which gets loaded by SAGA (i.e. by the
    SAGA engine), and which registers the CPI implementation classes which
    provide the adaptor's functionality.

    We only need one instance of this adaptor per process (actually per engine,
    but engine is a singleton, too...) -- the engine will though create new CPI
    implementation instances as needed (one per SAGA API object).
    '''

    __metaclass__ = Singleton


    def __init__ (self) :

        saga.cpi.base.AdaptorBase.__init__ (self, _adaptor_name, _adaptor_options)


    def register (self) :
        """ Adaptor registration function. The engine calls this during startup. 
    
            We usually do sanity checks here and throw and exception if we think
            the adaptor won't work in a given environment. In that case, the
            engine won't add it to it's internal list of adaptors. If everything
            is ok, we return the adaptor info.
        """
    
        return _adaptor_info


###############################################################################
#
class LocalJobService (saga.cpi.job.Service) :
    """ Implements saga.cpi.job.Service
    """
    def __init__ (self, api, adaptor) :

        """ Implements saga.cpi.job.Service.__init__
        """
        saga.cpi.Base.__init__ (self, api, adaptor, 'LocalJobService')


    @SYNC
    def init_instance (self, rm_url, session) :
        """ Service instance constructor
        """
        # check that the hostname is supported
        fqhn = socket.gethostname()
        if rm_url.host != 'localhost' and rm_url.host != fqhn:
            message = "Only 'localhost' and '%s' hostnames supported by this adaptor'" % (fqhn)
            self._logger.warning(message)
            raise saga.BadParameter(message=message) 

        self._rm      = rm_url
        self._session = session

        # holds the jobs that were started via this instance
        self._jobs = dict() # {job_obj:id, ...}


    def _update_jobid(self, job_obj, job_id):
        """ Update the job id for a job object registered 
            with this service instance.

            This is a convenince method and not part of the CPI.
        """
        self._jobs[job_obj] = job_id 


    @SYNC
    def get_url (self) :
        """ Implements saga.cpi.job.Service.get_url()
        """
        return self._rm

    @SYNC
    def list(self):
        """ Implements saga.cpi.job.Service.list()
        """
        jobids = list()
        for (job_obj, job_id) in self._jobs.iteritems():
            if job_id is not None:
                jobids.append(job_id)
        return jobids

    @SYNC
    def create_job (self, jd) :
        """ Implements saga.cpi.job.Service.get_url()
        """
        # check that only supported attributes are provided
        for attribute in jd.list_attributes():
            if attribute not in _adaptor_capabilities['jd_attributes']:
                raise saga.BadParameter('JobDescription.%s is not supported by this adaptor' % attribute)
        
        # create and return the new job
        engine       = getEngine ()
        cpi_instance = engine.get_adaptor (self, 'saga.job.Job', self._rm.scheme, 
                                           None, _adaptor_name)

        cpi_instance._session        = self._session
        cpi_instance._jd             = jd
        cpi_instance._parent_service = self
        cpi_instance._container      = self

        cpi_instance.init_instance ()

        job = saga.job.Job (_cpi_instance=cpi_instance)

        return job

    @SYNC
    def get_job (self, jobid):
        """ Implements saga.cpi.job.Service.get_url()
        """
        if jobid not in self._jobs.values():
            message = "This Service instance doesn't know a Job with ID '%s'" % (jobid)
            self._logger.error(message)
            raise saga.BadParameter(message=message) 
        else:
            for (job_obj, job_id) in self._jobs.iteritems():
                if job_id == jobid:
                    return job_obj._api


    def container_run (self, jobs) :
        self._logger.debug("container run: %s"  %  str(jobs))
        #raise saga.NoSuccess("Ole is lazy...")


    def container_wait (self, jobs, mode) :
        self._logger.debug("container wait: %s"  %  str(jobs))

        for ajob in jobs:
            ajob.wait()


        #raise saga.NoSuccess("Ole is lazy...")


    def container_cancel (self, jobs) :
        self._logger.debug("container cancel: %s"  %  str(jobs))
        raise saga.NoSuccess("Ole is lazy...");


    #def container_get_states (self, jobs) :
    #    self._logger.debug("container get_states: %s"  %  str(jobs))
    #    raise saga.NoSuccess("Ole is lazy...");


###############################################################################
#
class LocalJob (saga.cpi.job.Job) :
    """ Implements saga.cpi.job.Job
    """
    def __init__ (self, api, adaptor) :
        """ Implements saga.cpi.job.Job.__init__()
        """
        saga.cpi.Base.__init__ (self, api, adaptor, 'LocalJob')

    @SYNC
    def init_instance (self):
        """ Implements saga.cpi.job.Job.init_instance()
        """

        self._id         = None
        self._state      = saga.job.NEW
        self._returncode = None
        
        # The subprocess handle
        self._process    = None

        # register ourselves with the parent service
        # our job id is still None at this point
        self._parent_service._update_jobid (self, None)


    @SYNC
    def get_state(self):
        """ Implements saga.cpi.job.Job.get_state()
        """
        if self._state == saga.job.RUNNING:
            # only update if still running 
            self._returncode = self._process.poll() 
            if self._returncode is not None:
                if self._returncode != 0:
                    self._state = saga.job.FAILED
                else:
                    self._state = saga.job.DONE
        return self._state

    @SYNC
    def wait(self, timeout):
        if self._process is None:
            message = "Can't wait for job. Job has not been started"
            self._logger.warning(message)
            raise saga.IncorrectState(message)
        if timeout == -1:
            self._returncode = self._process.wait()
        else:
            t_beginning = time.time()
            seconds_passed = 0
            while True:
                self._returncode = self._process.poll()
                if self._returncode is not None:
                    break
                seconds_passed = time.time() - t_beginning
                if timeout and seconds_passed > timeout:
                    break
                time.sleep(0.5)

    @SYNC
    def get_id (self) :
        """ Implements saga.cpi.job.Job.get_id()
        """        
        return self._id

    @SYNC
    def get_exit_code(self) :
        """ Implements saga.cpi.job.Job.get_exit_code()
        """        
        return self._returncode

    @SYNC
    def cancel(self, timeout):
        try:
            os.killpg(self._process.pid, signal.SIGTERM)
            self._returncode = self._process.wait() # should return with the rc
            self._state = saga.job.CANCELED
        except OSError, ex:
            raise saga.IncorrectState("Couldn't cancel job %s: %s" % (self._id, ex))


    @SYNC
    def run(self): 
        """ Implements saga.cpi.job.Job.run()
        """
        # lots of attribute checking and such 
        executable  = self._jd.executable
        arguments   = self._jd.arguments
        environment = self._jd.environment
        cwd         = self._jd.working_directory
        
        # check if we want to write stdout to a file
        if self._jd.output is not None:
            if os.path.isabs(self._jd.output):
                self._job_output = open(jd.output,"w")  
            else:
                if cwd is not None:
                    self._job_output = open(os.path.join(cwd, self._jd.output),"w")
                else:
                    self._job_output = open(self._jd.output,"w")  
        else:
            self._job_output = None 

        # check if we want to write stderr to a file
        if self._jd.error is not None:
            if os.path.isabs(self._jd.error):
                self._job_error = open(self._jd.error,"w")  
            else:
                if cwd is not None:
                    self._job_error = open(os.path.join(self.cwd, self._jd.error),"w")
                else:
                    self._job_error = open(self._jd.error,"w") 
        else:
            self._job_error = None

        # check if we want to execute via mpirun
        if self._jd.spmd_variation is not None:
            if jd.spmd_variation.lower() == "mpi":
                if self._jd.number_of_processes is not None:
                    self.number_of_processes = self._jd.number_of_processes
                    use_mpirun = True
                self._logger.info("SPMDVariation=%s requested. Job will execute via 'mpirun -np %d'." % (self._jd.spmd_variation, self.number_of_processes))
            else:
                self._logger.warning("SPMDVariation=%s: unsupported SPMD variation. Ignoring." % self._jd.spmd_variation)
        else:
            use_mpirun = False

        # check if executable exists.
        if which(executable) == None:
            message = "Executable '%s' doesn't exist or is not in the path" % executable
            self._logger.error(message)        
            raise saga.BadParameter(message)

        # check if you can do mpirun
        if use_mpirun is True:
            which('mpirun')
            if mpirun == None:
                message = "SPMDVariation=MPI set, but can't find 'mpirun' executable."
                self._logger.error(message)        
                raise saga.BadParameter(message) 
            else:
                cmdline = '%s -np %d %s' % (mpirun, self.number_of_processes, str(self.executable))
        else:
            cmdline = str(executable)
        args = ""
        if arguments is not None:
            for arg in arguments:
                cmdline += " %s" % arg 

        # now we can finally try to run the job via subprocess
        try:
            self._logger.debug("Trying to execute: %s" % cmdline) 
            self._process = subprocess.Popen(cmdline, shell=True, 
                                             stderr=self._job_error, 
                                             stdout=self._job_output, 
                                             env=environment,
                                             cwd=cwd,
                                             preexec_fn=os.setsid)
            self._pid = self._process.pid
            self._state = saga.job.RUNNING

            jid = JobId()
            jid.native_id = self._pid
            jid.backend_url = str(self._parent_service.get_url())
            self._id = str(jid)
            self._parent_service._update_jobid(self, self._id)

        except Exception, ex:
            raise saga.NoSuccess(str(ex))

