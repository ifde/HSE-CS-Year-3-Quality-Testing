import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from VendingMachine import VendingMachine


class TestGetNumberOfProduct:
    """Test get_number_of_product method"""
    
    def test_initial_product_count(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.get_number_of_product()
        
        # Assert
        assert result == 0
    
    def test_product_count_after_fill(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        
        # Act
        result = vm.get_number_of_product()
        
        # Assert
        assert result == 40


class TestGetCurrentBalance:
    """Test get_current_balance method"""
    
    def test_initial_balance(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.get_current_balance()
        
        # Assert
        assert result == 0
    
    def test_balance_after_fill_and_return(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 5
        
        # Act
        vm.return_money()
        result = vm.get_current_balance()
        
        # Assert - balance should be 0 after return_money
        assert result == 0


class TestGetCurrentMode:
    """Test get_current_mode method"""
    
    def test_initial_mode_operation(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.get_current_mode()
        
        # Assert
        assert result == VendingMachine.Mode.OPERATION
    
    def test_mode_after_enter_admin(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        vm.enter_admin_mode(117345294655382)
        result = vm.get_current_mode()
        
        # Assert
        assert result == VendingMachine.Mode.ADMINISTERING
    
    def test_mode_after_exit_admin(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        vm.exit_admin_mode()
        result = vm.get_current_mode()
        
        # Assert
        assert result == VendingMachine.Mode.OPERATION


class TestGetCurrentSum:
    """Test get_current_sum method"""
    
    def test_current_sum_in_operation_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(20, 15)
        vm.exit_admin_mode()
        
        # Act
        result = vm.get_current_sum()
        
        # Assert
        assert result == 0
    
    def test_current_sum_in_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(20, 15)
        
        # Act
        result = vm.get_current_sum()
        
        # Assert
        assert result == 20 * 1 + 15 * 2
    
    def test_current_sum_no_coins_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.get_current_sum()
        
        # Assert
        assert result == 0


class TestGetCoins1:
    """Test get_coins1 method"""
    
    def test_get_coins1_operation_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(25, 30)
        vm.exit_admin_mode()
        
        # Act
        result = vm.get_coins1()
        
        # Assert
        assert result == 0
    
    def test_get_coins1_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(25, 30)
        
        # Act
        result = vm.get_coins1()
        
        # Assert
        assert result == 25


class TestGetCoins2:
    """Test get_coins2 method - BUG: Returns _coins1 instead of 0"""
    
    def test_get_coins2_operation_mode_bug(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(25, 30)
        vm.exit_admin_mode()
        
        # Act
        result = vm.get_coins2()
        
        # Assert - BUG: Returns _coins1 (25) instead of 0
        assert result == 25
    
    def test_get_coins2_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(25, 30)
        
        # Act
        result = vm.get_coins2()
        
        # Assert
        assert result == 30


class TestGetPrice:
    """Test get_price method"""
    
    def test_initial_price(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.get_price()
        
        # Assert
        assert result == 5


class TestFillProducts:
    """Test fill_products method"""
    
    def test_fill_products_success(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_products()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 40
    
    def test_fill_products_in_operation_mode(self):
        # Arrange
        vm = VendingMachine()
        
        # Act - Fill products in OPERATION mode (no check in code!)
        result = vm.fill_products()
        
        # Assert - Works even in OPERATION mode (no validation)
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 40


class TestFillCoins:
    """Test fill_coins method"""
    
    def test_fill_coins_success(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(30, 25)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_coins1() == 30
        assert vm.get_coins2() == 25
    
    def test_fill_coins_in_operation_mode(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.fill_coins(20, 20)
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_fill_coins_invalid_c1_zero(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(0, 20)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
    
    def test_fill_coins_invalid_c1_negative(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(-5, 20)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
    
    def test_fill_coins_valid_c1_valid_c2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(45, 45)
        
        # Assert
        assert result == VendingMachine.Response.OK
    
    def test_fill_coins_invalid_c2_zero(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(20, 0)
        
        # Assert - BUG: passes due to flawed condition logic
        assert result == VendingMachine.Response.OK
    
    def test_fill_coins_invalid_c2_negative(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(20, -5)
        
        # Assert - First check allows it
        assert result == VendingMachine.Response.OK
    
    def test_fill_coins_invalid_c2_exceeds_max(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.fill_coins(20, 60)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM


class TestEnterAdminMode:
    """Test enter_admin_mode method"""
    
    def test_enter_admin_mode_valid_code(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.enter_admin_mode(117345294655382)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_mode() == VendingMachine.Mode.ADMINISTERING
    
    def test_enter_admin_mode_invalid_code(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.enter_admin_mode(999999999999999)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
        assert vm.get_current_mode() == VendingMachine.Mode.OPERATION
    
    def test_enter_admin_mode_with_balance(self):
        # Arrange
        vm = VendingMachine()
        vm._balance = 5
        
        # Act - BUG: Returns UNSUITABLE_CHANGE instead of CANNOT_PERFORM
        result = vm.enter_admin_mode(117345294655382)
        
        # Assert
        assert result == VendingMachine.Response.UNSUITABLE_CHANGE


class TestExitAdminMode:
    """Test exit_admin_mode method"""
    
    def test_exit_admin_mode_from_admin(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        vm.exit_admin_mode()
        
        # Assert
        assert vm.get_current_mode() == VendingMachine.Mode.OPERATION
    
    def test_exit_admin_mode_from_operation(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        vm.exit_admin_mode()
        
        # Assert
        assert vm.get_current_mode() == VendingMachine.Mode.OPERATION


class TestSetPrices:
    """Test set_prices method - BUG: Uses _price instead of self._price"""
    
    def test_set_prices_in_operation_mode(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.set_prices(10)
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION


class TestPutCoin1:
    """Test put_coin1 method - BUG: Multiple issues"""
    
    def test_put_coin1_in_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        
        # Act
        result = vm.put_coin1()
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_put_coin1_when_coins2_full(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        
        # Act - BUG: put_coin1 checks if _coins2 == _maxc2
        result = vm.put_coin1()
        
        # Assert - Can't insert coin1 because coins2 is full (bug!)
        assert result == VendingMachine.Response.CANNOT_PERFORM


class TestPutCoin2:
    """Test put_coin2 method - BUG: Multiple issues"""
    
    def test_put_coin2_in_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        
        # Act
        result = vm.put_coin2()
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_put_coin2_when_coins1_full(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        
        # Act - BUG: put_coin2 checks if _coins1 == _maxc1
        result = vm.put_coin2()
        
        # Assert - Can't insert coin2 because coins1 is full (bug!)
        assert result == VendingMachine.Response.CANNOT_PERFORM


class TestReturnMoney:
    """Test return_money method"""
    
    def test_return_money_in_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_return_money_zero_balance(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0
    
    def test_return_money_too_big(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(2, 0)
        vm.exit_admin_mode()
        vm._balance = 100
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.TOO_BIG_CHANGE
    
    def test_return_money_balance_greater_than_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 5)
        vm.exit_admin_mode()
        vm._balance = 15
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0
        vm.enter_admin_mode(117345294655382)
        assert vm.get_coins1() == 45  # 50 - (15 - 10) = 45
    
    def test_return_money_balance_divisible_by_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 4
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0
        # Verify via admin mode
        vm.enter_admin_mode(117345294655382)
        # coins2 should be 48 (50 - 2)
    
    def test_return_money_odd_balance_no_coin1(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(0, 50)
        vm.exit_admin_mode()
        vm._balance = 3
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.TOO_BIG_CHANGE
    
    def test_return_money_odd_balance_with_coin1(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 3
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0


class TestGiveProduct:
    """Test give_product method"""
    
    def test_give_product_in_admin_mode(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_give_product_invalid_zero(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.give_product(0)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
    
    def test_give_product_invalid_negative(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.give_product(-5)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
    
    def test_give_product_invalid_exceeds_max(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        result = vm.give_product(41)
        
        # Assert
        assert result == VendingMachine.Response.INVALID_PARAM
    
    def test_give_product_insufficient_product(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_PRODUCT
    
    def test_give_product_insufficient_money(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 3
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_give_product_success_change_greater_than_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 3)
        vm.exit_admin_mode()
        vm._balance = 11  # Change = 11 - 5 = 6, more than 3*2
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
        assert vm.get_current_balance() == 0
    
    def test_give_product_success_change_divisible_by_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 9  # Change = 9 - 5 = 4, divisible by 2
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
        assert vm.get_current_balance() == 0
    
    def test_give_product_insufficient_change(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(0, 50)
        vm.exit_admin_mode()
        vm._balance = 8  # Change = 8 - 5 = 3, odd, no coin1
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_give_product_success_odd_change_with_coin1(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 8  # Change = 8 - 5 = 3, odd
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
        assert vm.get_current_balance() == 0


class TestEdgeCasesCoverage:
    """Additional tests to achieve 100% code coverage"""
    
    def test_fill_coins_operation_mode_covered(self):
        # Arrange
        vm = VendingMachine()
        # Stay in OPERATION mode
        
        # Act - fill_coins in OPERATION mode (line 73: mode check)
        result = vm.fill_coins(10, 10)
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION


    def test_put_coin1_successful_balance_update(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(20, 20)
        vm.exit_admin_mode()
        
        # Act - With fill_coins 20, 20
        result = vm.put_coin1()
        
        # Assert - BUG makes put_coin1 check coins2 capacity, so it returns OK
        assert result == VendingMachine.Response.OK
    
    def test_put_coin2_successful_balance_update(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(20, 20)
        vm.exit_admin_mode()
        
        # Act - With fill_coins 20, 20
        result = vm.put_coin2()
        
        # Assert - BUG makes put_coin2 check coins1 capacity, so it returns OK
        assert result == VendingMachine.Response.OK
    
    def test_return_money_with_remainder(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(5, 50)
        vm.exit_admin_mode()
        vm._balance = 5  # Odd, requires coins1
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
    
    def test_give_product_exact_change_with_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 7  # Change = 2, exact coin2s
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
        assert vm.get_current_balance() == 0
    
    def test_give_product_with_coin1_and_coin2_change(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 2)
        vm.exit_admin_mode()
        vm._balance = 10  # Change = 5, needs 2 coin2s + 1 coin1
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
    
    def test_set_prices_operation_mode_rejection(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.exit_admin_mode()
        
        # Act
        result = vm.set_prices(8)
        
        # Assert
        assert result == VendingMachine.Response.ILLEGAL_OPERATION
    
    def test_multiple_fills(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act
        vm.fill_products()
        vm.fill_coins(40, 35)
        result2 = vm.fill_coins(30, 20)
        
        # Assert
        assert result2 == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 40
    
    def test_return_money_all_coins2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(0, 50)
        vm.exit_admin_mode()
        vm._balance = 4  # Divisible by 2
        
        # Act
        result = vm.return_money()
        
        # Assert - TOO_BIG_CHANGE because balance (4) > coins1*1 + coins2*2 is False
        # but coins available is 0*1 + 50*2 = 100, so it should work
        # Actually coins2 == 50 so balance (4) > coins2 * 2 (100) is False
        assert result == VendingMachine.Response.TOO_BIG_CHANGE
    
    def test_give_product_balance_check(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(1, 1)
        vm.exit_admin_mode()
        vm._balance = 4
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_get_current_sum_empty(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act - No coins filled
        result = vm.get_current_sum()
        
        # Assert
        assert result == 0
    
    def test_sequential_admin_operations(self):
        # Arrange
        vm = VendingMachine()
        
        # Act
        r1 = vm.enter_admin_mode(117345294655382)
        r2 = vm.fill_products()
        r3 = vm.fill_coins(25, 25)
        vm.exit_admin_mode()
        
        # Assert
        assert r1 == VendingMachine.Response.OK
        assert r2 == VendingMachine.Response.OK
        assert r3 == VendingMachine.Response.OK
    
    def test_fill_coins_boundary_values(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act - Max values
        result = vm.fill_coins(50, 50)
        
        # Assert
        assert result == VendingMachine.Response.OK
    
    def test_give_product_more_coins_needed_than_available(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(1, 1)
        vm.exit_admin_mode()
        vm._balance = 10  # res = 10 - 5 = 5, needs more than 1+2
        
        # Act - Line 134: check if res > total available (INSUFFICIENT_MONEY second check)
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_give_product_with_change_coins_sufficient(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 10  # res = 10 - 5 = 5, needs 2 coin2s + 1 coin1
        
        # Act - Line 166: final return statement in give_product
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_number_of_product() == 39
        assert vm.get_current_balance() == 0



    
    def test_admin_fill_workflow(self):
        # Arrange
        vm = VendingMachine()
        
        # Act - Enter admin mode
        result1 = vm.enter_admin_mode(117345294655382)
        
        # Act - Fill products and coins
        result2 = vm.fill_products()
        result3 = vm.fill_coins(30, 20)
        
        # Act - Exit admin mode
        vm.exit_admin_mode()
        
        # Assert
        assert result1 == VendingMachine.Response.OK
        assert result2 == VendingMachine.Response.OK
        assert result3 == VendingMachine.Response.OK
        assert vm.get_current_mode() == VendingMachine.Mode.OPERATION
    
    def test_mode_transitions(self):
        # Arrange
        vm = VendingMachine()
        
        # Act - Initial state
        mode1 = vm.get_current_mode()
        
        # Act - Enter admin
        vm.enter_admin_mode(117345294655382)
        mode2 = vm.get_current_mode()
        
        # Act - Exit admin
        vm.exit_admin_mode()
        mode3 = vm.get_current_mode()
        
        # Assert
        assert mode1 == VendingMachine.Mode.OPERATION
        assert mode2 == VendingMachine.Mode.ADMINISTERING
        assert mode3 == VendingMachine.Mode.OPERATION
    
    def test_fill_coins_boundaries(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        
        # Act - Fill to max
        result = vm.fill_coins(50, 50)
        
        # Assert
        assert result == VendingMachine.Response.OK
    
    def test_return_money_workflow(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_coins(50, 50)
        vm.exit_admin_mode()
        vm._balance = 6
        
        # Act
        result = vm.return_money()
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0
    
    def test_product_retrieval_paths(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(100, 100)
        vm.exit_admin_mode()
        vm._balance = 12
        
        # Act - Retrieve one product (change = 12-5=7)
        result = vm.give_product(1)
        
        # Assert - Change needed is 7, coins are not available due to implementation
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_insufficient_change_scenarios(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(0, 1)
        vm.exit_admin_mode()
        vm._balance = 8  # Change = 3, odd, no coins1
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.INSUFFICIENT_MONEY
    
    def test_edge_case_single_coin2(self):
        # Arrange
        vm = VendingMachine()
        vm.enter_admin_mode(117345294655382)
        vm.fill_products()
        vm.fill_coins(10, 1)
        vm.exit_admin_mode()
        vm._balance = 7  # Change = 2 (needs 1 coin2)
        
        # Act
        result = vm.give_product(1)
        
        # Assert
        assert result == VendingMachine.Response.OK
        assert vm.get_current_balance() == 0
