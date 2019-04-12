// LeanCoins ICO  https://remix.ethereum.org/

// Version of compiler
pragma solidity ^0.4.24;

contract leancoin_ico {
    
    // Introducing max amount of LeanCoins available on ICO
    uint public max_leancoins = 1000000;
    
    // Conversion rate LeCo/EUR :) 
    uint public eur_to_leancoins = 1000;
    
    // Amount o LeanCoins bought by investors
    uint public total_leancoins_bought = 0;
    
    // Investor address --> equity mapping(input-output)
    mapping(address => uint) equity_leancoins;
    mapping(address => uint) equity_eur;
    
    // LeanCoin availability check
    modifier can_buy_leancoins(uint eur_invested) {
        require (eur_invested * eur_to_leancoins + total_leancoins_bought <= max_leancoins);
        _;
    }
    
    // Return investor's equity amount (LeanCoins)
    function equity_in_leancoins(address investor) external constant returns (uint) {
        return equity_leancoins[investor];
    }
    
    // Return investor's equity amount (EUR)
        function equity_in_eur(address investor) external constant returns (uint) {
        return equity_eur[investor];
    }
    
    // Buy LeanCoins 
    function buy_leancoins(address investor, uint eur_invested) external
    can_buy_leancoins(eur_invested) {
        uint leancoins_bought = eur_invested * eur_to_leancoins;
        equity_leancoins[investor] += leancoins_bought;
        equity_eur[investor] = equity_leancoins[investor] / 1000; // (1000 as inverted conversion rate)
        total_leancoins_bought += leancoins_bought;
    }
    
    // Sell LeanCoins (Buyback)
    function sell_leancoins(address investor, uint leancoins_sold) external {
        equity_leancoins[investor] -= leancoins_sold;
        equity_eur[investor] = equity_leancoins[investor] / 1000; // (1000 as inverted conversion rate)
        total_leancoins_bought -= leancoins_sold;
    }
}




