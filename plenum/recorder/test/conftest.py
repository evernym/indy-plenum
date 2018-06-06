import math

from plenum.recorder.test.helper import create_recorder_for_test

from plenum.test.conftest import *  # noqa
from plenum.common.util import randomString
from plenum.test.pool_transactions.helper import sdk_add_new_nym
from plenum.test.helper import sdk_send_random_and_check



# overriddenConfigValues['USE_WITH_STACK'] = 1
#
#
# @pytest.fixture(scope="module")
# def tconf(general_conf_tdir):
#     conf = _tconf(general_conf_tdir)
#     reload_modules_for_recorder(conf)
#     return conf

TOTAL_TXNS = 2


@pytest.fixture(scope="module")
def some_txns_done(txnPoolNodesLooper, txnPoolNodeSet, sdk_pool_handle,
                   sdk_wallet_steward):
    for i in range(math.ceil(TOTAL_TXNS / 2)):
        sdk_add_new_nym(txnPoolNodesLooper, sdk_pool_handle, sdk_wallet_steward,
                        alias='testSteward' + randomString(100))
    for i in range(math.floor(TOTAL_TXNS / 2)):
        sdk_send_random_and_check(txnPoolNodesLooper, txnPoolNodeSet,
                                  sdk_pool_handle, sdk_wallet_steward, 5)


@pytest.fixture()
def recorder(tmpdir_factory):
    return create_recorder_for_test(tmpdir_factory, 'test_db')