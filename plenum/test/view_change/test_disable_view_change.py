import pytest
from plenum.test.helper import waitForViewChange
from plenum.test.view_change.helper import simulate_slow_master


@pytest.fixture(scope="module")
def disable_view_change_config(tconf):
    tconf.unsafe.add('disable_view_change')
    yield tconf
    tconf.unsafe.remove('disable_view_change')


def test_disable_view_change(
        disable_view_change_config,
        looper,
        txnPoolNodeSet,
        viewNo,
        sdk_pool_handle,
        sdk_wallet_steward):
    assert disable_view_change_config
    assert isinstance(disable_view_change_config.unsafe, set)
    assert 'disable_view_change' in disable_view_change_config.unsafe

    simulate_slow_master(looper, txnPoolNodeSet,
                         sdk_pool_handle,
                         sdk_wallet_steward)

    with pytest.raises(AssertionError):
        waitForViewChange(looper, txnPoolNodeSet, expectedViewNo=viewNo + 1)
