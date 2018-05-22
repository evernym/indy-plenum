from plenum.recorder.test.helper import reload_modules_for_replay, \
    get_replayable_node_class, create_replayable_node_and_check
from plenum.test.helper import sdk_send_random_and_check
from plenum.test.node_catchup.helper import ensure_all_nodes_have_same_data
from plenum.test.test_node import ensureElectionsDone
from plenum.test.view_change.helper import ensure_view_change
from plenum.test.view_change.conftest import viewNo # noqa


TestRunningTimeLimitSec = 550

whitelist = ['cannot find remote with name']


def test_view_change_after_some_txns(txnPoolNodesLooper, txnPoolNodeSet,
                                     some_txns_done, testNodeClass, viewNo,
                                     sdk_pool_handle, sdk_wallet_client,
                                     node_config_helper_class, tconf, tdir,
                                     allPluginsPath, tmpdir_factory):
    """
    Check that view change is done after processing some of txns
    """
    ensure_view_change(txnPoolNodesLooper, txnPoolNodeSet)
    ensureElectionsDone(looper=txnPoolNodesLooper, nodes=txnPoolNodeSet)
    ensure_all_nodes_have_same_data(txnPoolNodesLooper, nodes=txnPoolNodeSet)

    sdk_send_random_and_check(txnPoolNodesLooper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 10)
    ensure_all_nodes_have_same_data(txnPoolNodesLooper, txnPoolNodeSet)

    for node in txnPoolNodeSet:
        txnPoolNodesLooper.removeProdable(node)

    reload_modules_for_replay(tconf)

    replayable_node_class, basedirpath = get_replayable_node_class(
        tmpdir_factory, tdir, testNodeClass)

    for node in txnPoolNodeSet:
        node.stop()

    print('-------------Replaying now---------------------')

    for node in txnPoolNodeSet:
        create_replayable_node_and_check(txnPoolNodesLooper, txnPoolNodeSet,
                                         node, replayable_node_class,
                                         node_config_helper_class, tconf,
                                         basedirpath, allPluginsPath)
