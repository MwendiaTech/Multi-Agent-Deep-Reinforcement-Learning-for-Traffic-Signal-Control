Example for sumo build try
==========================

.. _example-sumo-build-try:

Since the report of the "try" command may be complex, here is an example.

The verbosity of the command is configured with option "``--detail``". This
option takes an integer between 0 and 3. 0 gives the shortest report, 3 the
most detailed.

We assume that you have a list of module specifications in a configuration file
in your application that sumo loads automatically. For examples on
configuration files see also :ref:`sumo.config examples
<configuration-files-config-examples>`. 

We start the program in our application top directory like this::

  sumo build try

The output of the program looks like this::

  Not all modules have exactly specified versions. These modules need an 
  exact version specification:
      ALARM
  
  Not all dependencies were included in module specifications, these modules
  have to be added:
      BSPDEP
      MISC
  
  Command 'new' would create build with tag 'AUTO-003'
  
  Your module specifications are still incomplete, command 'new' can not
  be used with these.

This means that the modules "``BSPDEP``" and "``MISC``" are needed by other modules and have to be added to your module specifications. "``ALARM``" is in your list of specifications but is mission a versionname.

We can see more detail if we start the same command with "``--detail 1``"::

  sumo build try --detail 1

The output of the program now looks like this::

  Possible versions for unspecified/missing modules:
  
  ALARM               R3-0 R3-1 R3-2 R3-3 R3-4 R3-5 R3-7 R3-8
  BSPDEP              R3-0 R3-1 R3-2 R3-3
  MISC                R2-1 R2-2 R2-3 R2-4 TAGLESS-2-0
  
  Not all modules have exactly specified versions. These modules need an 
  exact version specification:
      ALARM
  
  Not all dependencies were included in module specifications, these modules
  have to be added:
      BSPDEP
      MISC
  
  Command 'new' would create build with tag 'AUTO-003'
  
  Your module specifications are still incomplete, command 'new' can not
  be used with these.

Here we see possible versionnames for the modules that are not have to version
or are not in the module specification list.

In this example we specify to use "``ALARM:R3-2``" and "``MISC:R2-4``". For "``BSPDEP``" we want to see more detail than just the list of known version. We start sumo again with "``--detail 2``"::

  sumo build try --detail 2

The output of the program now looks like this::

  Details on unspecified/missing modules:
  
  {
      "BSPDEP": {
          "R3-0": {
              "built": false,
              "dependents": {
                  "ALARM:R3-2": "state: not tested"
              }
          },
          "R3-1": {
              "built": false,
              "dependents": {
                  "ALARM:R3-2": "state: not tested"
              }
          },
          "R3-2": {
              "built": false,
              "dependents": {
                  "ALARM:R3-2": "state: not tested"
              }
          },
          "R3-3": {
              "built": false,
              "dependents": {
                  "ALARM:R3-2": "state: not tested"
              }
          }
      }
  }
  
  Not all dependencies were included in module specifications, these modules
  have to be added:
      BSPDEP
  
  Command 'new' would create build with tag 'AUTO-003'
  
  Your module specifications are still incomplete, command 'new' can not
  be used with these.

The detail section of the output shows information on the missing modules in
JSON format. There is a map that contains a key for each missing module or
modules whose version is not specified. The values are maps with two keys:

built:
  This shows if the supports has been successfully built. This information is
  taken from the build database file and, if provided, the scan database file.
  The value is either "``true``" or "``false``".

dependents:
  This shows the modules that depend on the given module. In the example above
  we see that ALARM:R3-2 depends on BSPDEP:R3-0, BSPDEP:R3-1, BSPDEP:R3-2 or
  BSPDEP:R3-3. The string "state: not tested" shows if there exists a build
  where both modules were built together. On this case, there is no such build.
  Otherwise the string could be "state: <STATE>" where <STATE> is the state of
  the build where both modules are part of.

We add BSPDEP:R3-3 to our module specifications and start sumo again::

  sumo build try --detail 2

The output is now::

  Command 'new' would create build with tag 'AUTO-003'
  
  Your module specifications are complete. You can use these with command
  'new' to create a new build.

The detail section is not printed since our module specifications are complete.

In order to see the detail section anyway, we use "``--detail 3``"::

  sumo build try --detail 3

The output is now::

  Details on all modules:
  
  {
      "ALARM": {
          "R3-2": {
              "built": false,
              "dependents": {
                  "MCAN:R2-6-4": "state: not tested"
              }
          }
      },
      "BASE": {
          "R3-14-12-2-1-aragon6": {
              "built": true,
              "dependents": {
                  "ALARM:R3-2": "state: not tested",
                  "BSPDEP:R3-3": "state: not tested",
                  "BSPDEP_TIMER:R6-2": "state: testing",
                  "BSPDEP_VMETAS:R2-0": "state: testing",
                  "MCAN:R2-6-4": "state: not tested",
                  "MISC:R2-4": "state: not tested",
                  "MISC_DBC:R3-0": "state: testing",
                  "MISC_DEBUGMSG:R3-0": "state: testing",
                  "SOFT_DEVHWCLIENT:R3-0": "state: testing"
              }
          }
      },
      "BSPDEP": {
          "R3-3": {
              "built": false,
              "dependents": {
                  "ALARM:R3-2": "state: not tested"
              }
          }
      },
      "BSPDEP_TIMER": {
          "R6-2": {
              "built": true,
              "dependents": {
                  "BSPDEP:R3-3": "state: not tested"
              }
          }
      },
      "BSPDEP_VMETAS": {
          "R2-0": {
              "built": true,
              "dependents": {
                  "MCAN:R2-6-4": "state: not tested"
              }
          }
      },
      "MCAN": {
          "R2-6-4": {
              "built": false
          }
      },
      "MISC": {
          "R2-4": {
              "built": true,
              "dependents": {
                  "ALARM:R3-2": "state: not tested",
                  "BSPDEP:R3-3": "state: not tested"
              }
          }
      },
      "MISC_DBC": {
          "R3-0": {
              "built": true,
              "dependents": {
                  "MCAN:R2-6-4": "state: not tested"
              }
          }
      },
      "MISC_DEBUGMSG": {
          "R3-0": {
              "built": true,
              "dependents": {
                  "MCAN:R2-6-4": "state: not tested"
              }
          }
      },
      "SOFT_DEVHWCLIENT": {
          "R3-0": {
              "built": true,
              "dependents": {
                  "MCAN:R2-6-4": "state: not tested"
              }
          }
      }
  }
  
  Command 'new' would create build with tag 'AUTO-003'
  
  Your module specifications are complete. You can use these with command
  'new' to create a new build.

Since our module specifications are complete, we could now create a new build
with::

  sumo build new


