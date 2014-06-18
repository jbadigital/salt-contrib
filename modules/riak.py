'''
Support for riak
'''

import salt.utils


def __virtual__():
    '''
    Only load the module if riak is installed
    '''
    if salt.utils.which('riak'):
        return True
    return False


def version():
    '''
    Return Riak node version

    CLI Example::

    .. code-block:: bash

        salt '*' riak.version
    '''
    cmd = 'riak version'
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    return msgs[0]


def ping():
    if is_up() is True:
        return "pong"
    else:
        return ""


def is_up():
    '''
    Ping a Riak node to check its status

    CLI Example::

    .. code-block:: bash

        salt '*' riak.is_up
    '''
    return not bool(__salt__['cmd.retcode']('riak ping'))


def start():
    '''
    Start a Riak node. Returns True if the node is left in a running state.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.start
    '''
    return not bool(__salt__['cmd.retcode']('riak start'))


def stop():
    '''
    Stop a running Riak node. Returns True if the node is left in a stopped
    state.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.stop
    '''
    return not bool(__salt__['cmd.retcode']('riak stop'))


def restart():
    '''
    Stops and then starts the running Riak node without exiting the Erlang VM.
    Returns True if the node is left in a running state.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.restart
    '''
    return not bool(__salt__['cmd.retcode']('riak restart'))


def cluster_join(node):
    '''
    Join this node to the cluster containing <node>.

    node
        The full node name, in the form user@ip-address

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_join <node>
    '''
    if len(node.split("@")) != 2:
        return False
    cmd = 'riak-admin cluster join %s' % node
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0].startswith("Success"):
        return True
    else:
        return msgs[0]


def cluster_leave(node=None, force=False):
    '''
    Instruct this node to hand off its data partitions, leave the cluster and 
    shutdown.

    node
        The full node name, in the form user@ip-address.
        If this is not supplied, the node will attempt to remove itself.

    force
        Remove <node> from the cluster without first handing off data 
        partitions. This command is designed for crashed, unrecoverable nodes, 
        and should be used with caution.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_leave <node> [<force>]
    '''
    if node is not None and len(node.split("@")) != 2:
        return False
    if force == False:
        cmd = 'riak-admin cluster leave'
    else:
        cmd = 'riak-admin cluster force-remove'
    if node is not None:
        cmd = '%s %s' % (cmd, node)
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0].startswith("Success"):
        return True
    else:
        return msgs[0]


def cluster_replace(node1, node2, force=False):
    '''
    Instruct <node1> to transfer all data partitions to <node2>, then leave the
    cluster and shutdown.

    node1
        The full node name, in the form user@ip-address

    node2
        The full node name, in the form user@ip-address

    force
        Remove <node> from the cluster without first handing off data 
        partitions. This command is designed for crashed, unrecoverable nodes, 
        and should be used with caution.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_replace <node>
    '''
    if len(node1.split("@")) != 2 and len(node2.split("@")) != 2:
        return False
    cmd = 'riak-admin cluster replace %s %s' % (node1, node2)
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0].startswith("Success"):
        return True
    else:
        return msgs[0]


def cluster_plan():
    '''
    Display the currently staged cluster changes.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_plan
    '''
    cmd = 'riak-admin cluster plan'
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0] == "There are no staged changes":
        return None
    else:
        return msgs


def cluster_clear():
    '''
    Clear the currently staged cluster changes.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_clear
    '''
    cmd = 'riak-admin cluster clear'
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0] == "Cleared staged cluster changes":
        return True
    else:
        return msgs[0]


def cluster_commit():
    '''
    Commit the currently staged cluster changes.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.cluster_commit
    '''
    cmd = 'riak-admin cluster commit'
    out = __salt__['cmd.run'](cmd).split('\n')
    msgs = [line for line in out if not line.startswith("!!!!")]
    if len(msgs) > 0 and msgs[0].startswith("Attempting"):
        del(msgs[0])
    if msgs[0].startswith("You must verify the plan"):
        return cluster_plan()
    else:
        return msgs[0]


def ringready():
    '''
    Checks whether all nodes in the cluster agree on the ring state.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.ringready
    '''
    cmd = 'riak-admin ringready'
    out = __salt__['cmd.run'](cmd).split('\n')
    if len(out) > 0 and out[0].startswith("TRUE"):
        return True
    else:
        return False


def ring_status():
    '''
    Outputs the current claimant, its status, ringready, pending ownership 
    handoffs and a list of unreachable nodes.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.ring_status
    '''
    cmd = 'riak-admin ring-status'
    out = __salt__['cmd.run'](cmd).split('\n')
    out = out[1:len(out)]
    ret = []
    for line in out:
        if len(line) > 0 and line[:1] != "=" and line[:1] != " ":
            ret.append(line)
    return ret


def member_status():
    '''
    Get cluster member status

    CLI Example:

    .. code-block:: bash

        salt '*' riak.member_status
    '''
    ret = {'membership': {},
            'summary': {'Valid': 0,
                        'Leaving': 0,
                        'Exiting': 0,
                        'Joining': 0,
                        'Down': 0,
                        }
            }
    cmd = 'riak-admin member-status'
    out = __salt__['cmd.run'](cmd).splitlines()
    for line in out:
        if line.startswith(('=', '-', 'Status')):
            continue
        if '/' in line:
            # We're in the summary line
            comps = line.split('/')
            for item in comps:
                key, val = item.split(':')
                ret['summary'][key.strip()] = val.strip()
        vals = line.split()
        if len(vals) == 4:
            # We're on a node status line
            ret['membership'][vals[3]] = {'Status': vals[0],
                                          'Ring': vals[1],
                                          'Pending': vals[2],
                                          }
    return ret


def transfers():
    '''
    Identifies nodes that are awaiting transfer of one or more partitions.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.transfers
    '''
    cmd = 'riak-admin transfers'
    out = __salt__['cmd.run'](cmd).split('\n')
    if out[0] == "No transfers active":
        return out[0]
    else:
        return out


def diag():
    '''
    Run diagnostic checks against <node>.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.diag
    '''
    cmd = 'riak-admin diag'
    out = __salt__['cmd.run'](cmd).split('\n')
    if len(out) == 1 and len(out[0]) == 0:
        return "Nothing to report"
    else:
        return out


def status():
    '''
    Prints status information, including performance statistics, system health
    information, and version numbers.

    CLI Example::

    .. code-block:: bash

        salt '*' riak.status
    '''
    cmd = 'riak-admin status'
    out = __salt__['cmd.run'](cmd).split('\n')
    ret = []
    for line in out:
        parts = line.split(" : ")
        if len(parts) == 2:
            ret.append({parts[0]: parts[1]})
    return ret
