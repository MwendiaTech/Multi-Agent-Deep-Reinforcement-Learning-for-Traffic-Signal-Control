#!/bin/bash

SCRIPT_FULL_NAME=$(readlink -e $0)
MYDIR=$(dirname $SCRIPT_FULL_NAME)
MYNAME=$(basename $SCRIPT_FULL_NAME)

EPICS_VER=7.0

if [ "$1" == "-h" ]; then
    echo "$MYNAME: create files for sumo demo."
    exit 0
fi

# create apps directory:
mkdir -p apps

# create support directory:
mkdir -p support
cd support

# get and build EPICS base:
mkdir -p base
cd base

if [ ! -d "$EPICS_VER" ]; then
    git clone -b $EPICS_VER https://github.com/epics-base/epics-base.git $EPICS_VER
    cd $EPICS_VER && make -sj
fi
cd $MYDIR

# set environment for usage of EPICS base:
EPICS_HOST_ARCH=$(support/base/$EPICS_VER/startup/EpicsHostArch)
EPICS_SUPPORT=$PWD/support
EPICS_BASE=$PWD/support/base/$EPICS_VER
PATH=$EPICS_BASE/bin/$EPICS_HOST_ARCH:$PATH

# create "low" support:
cd support
if [ ! -d low ]; then
    mkdir -p low/1
    cd low/1

    makeBaseApp.pl -b $EPICS_BASE -t support low
    sed -i -e 's/#DB.*/DB += low.db/' lowApp/Db/Makefile
    mkdir -p db
    cat > lowApp/Db/low.db << END
record(calc, "low")
{
   field(CALC, "RNDM")
   field(SCAN, "1 second")
}
END
fi
cd $MYDIR

# create "high" support:
cd support
if [ ! -d high ]; then
    mkdir -p high/1
    cd high/1

    makeBaseApp.pl -b $EPICS_BASE -t support high
    sed -i -e 's/#DB.*/DB += high.db/' highApp/Db/Makefile
    cat > highApp/Db/high.db << END
record(calc, "high")
{
   field(CALC, "1000*RNDM")
   field(SCAN, "1 second")
}
END
sed -i -e "/^EPICS_BASE/a LOW=$EPICS_SUPPORT/low/1" configure/RELEASE
fi

cd $MYDIR

# create "app":
cd apps
if [ ! -d appA ]; then
    mkdir -p appA
    cd appA
    makeBaseApp.pl -b $EPICS_BASE -t ioc A
    makeBaseApp.pl -i -t ioc -p A iocA
    chmod u+x iocBoot/iocA/st.cmd
    sed -i -e 's/^#\(< envPaths\)/\1/' iocBoot/iocA/st.cmd
    sed -i -e '/^#dbLoadRecords/acd $(LOW)\ndbLoadRecords("db/low.db")\ncd $(HIGH)\ndbLoadRecords("db/high.db")\n' iocBoot/iocA/st.cmd
    cat > configure/RELEASE << END
HIGH=$EPICS_SUPPORT/high/1
LOW=$EPICS_SUPPORT/low/1
EPICS_BASE=$EPICS_BASE
END
fi

cd $MYDIR

make -C support/low/1 -sj
make -C support/high/1 -sj
make -C apps/appA -sj

