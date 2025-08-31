import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import Swal from 'sweetalert2';

const MetaMaskBuyer = ({ credit, onPurchaseSuccess }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [account, setAccount] = useState('');
  const [network, setNetwork] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);
  const [isPurchasing, setIsPurchasing] = useState(false);
  const [purchaseAmount, setPurchaseAmount] = useState(1);

  // Sepolia network configuration
  const SEPOLIA_CHAIN_ID = '0xaa36a7'; // 11155111 in hex
  const SEPOLIA_NETWORK = {
    chainId: SEPOLIA_CHAIN_ID,
    chainName: 'Sepolia Testnet',
    nativeCurrency: {
      name: 'Sepolia Ether',
      symbol: 'SEP',
      decimals: 18,
    },
    rpcUrls: ['https://rpc.sepolia.org'],
    blockExplorerUrls: ['https://sepolia.etherscan.io'],
  };

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    if (typeof window.ethereum !== 'undefined') {
      try {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        if (accounts.length > 0) {
          setAccount(accounts[0]);
          setIsConnected(true);
          checkNetwork();
        }
      } catch (error) {
        console.error('Error checking connection:', error);
      }
    }
  };

  const checkNetwork = async () => {
    try {
      const chainId = await window.ethereum.request({ method: 'eth_chainId' });
      if (chainId === SEPOLIA_CHAIN_ID) {
        setNetwork('Sepolia');
      } else {
        setNetwork('Wrong Network');
      }
    } catch (error) {
      console.error('Error checking network:', error);
    }
  };

  const connectWallet = async () => {
    if (typeof window.ethereum === 'undefined') {
      Swal.fire({
        icon: 'error',
        title: 'MetaMask Not Found',
        text: 'Please install MetaMask to use this feature.',
        footer: '<a href="https://metamask.io/" target="_blank">Install MetaMask</a>'
      });
      return;
    }

    setIsConnecting(true);
    try {
      // Request account access
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      setAccount(accounts[0]);
      setIsConnected(true);
      
      // Check and switch to Sepolia if needed
      await switchToSepolia();
      
    } catch (error) {
      console.error('Error connecting wallet:', error);
      Swal.fire({
        icon: 'error',
        title: 'Connection Failed',
        text: 'Failed to connect MetaMask wallet.',
      });
    } finally {
      setIsConnecting(false);
    }
  };

  const switchToSepolia = async () => {
    try {
      const chainId = await window.ethereum.request({ method: 'eth_chainId' });
      
      if (chainId !== SEPOLIA_CHAIN_ID) {
        try {
          await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: SEPOLIA_CHAIN_ID }],
          });
        } catch (switchError) {
          // This error code indicates that the chain has not been added to MetaMask
          if (switchError.code === 4902) {
            try {
              await window.ethereum.request({
                method: 'wallet_addEthereumChain',
                params: [SEPOLIA_NETWORK],
              });
            } catch (addError) {
              console.error('Error adding Sepolia network:', addError);
              Swal.fire({
                icon: 'error',
                title: 'Network Error',
                text: 'Failed to add Sepolia network to MetaMask.',
              });
            }
          }
        }
      }
      
      await checkNetwork();
    } catch (error) {
      console.error('Error switching network:', error);
    }
  };

  const purchaseCredit = async () => {
    if (!isConnected) {
      Swal.fire({
        icon: 'warning',
        title: 'Wallet Not Connected',
        text: 'Please connect your MetaMask wallet first.',
      });
      return;
    }

    if (network !== 'Sepolia') {
      Swal.fire({
        icon: 'warning',
        title: 'Wrong Network',
        text: 'Please switch to Sepolia testnet to purchase credits.',
      });
      return;
    }

    if (purchaseAmount <= 0 || purchaseAmount > credit.amount) {
      Swal.fire({
        icon: 'error',
        title: 'Invalid Amount',
        text: `Please enter a valid amount between 1 and ${credit.amount} kg.`,
      });
      return;
    }

    setIsPurchasing(true);
    try {
      // Calculate total cost in ETH
      const totalCost = purchaseAmount * credit.price;
      
      // Show confirmation dialog
      const result = await Swal.fire({
        icon: 'question',
        title: 'Confirm Purchase',
        html: `
          <div class="text-left">
            <p><strong>Credit:</strong> ${credit.name}</p>
            <p><strong>Amount:</strong> ${purchaseAmount} kg</p>
            <p><strong>Price per kg:</strong> ${credit.price} ETH</p>
            <p><strong>Total Cost:</strong> ${totalCost.toFixed(4)} ETH</p>
            <p><strong>Network:</strong> Sepolia Testnet</p>
          </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Purchase',
        cancelButtonText: 'Cancel',
        confirmButtonColor: '#10B981',
        cancelButtonColor: '#6B7280',
      });

      if (result.isConfirmed) {
        // Simulate blockchain transaction
        await simulateTransaction(totalCost);
        
        // Call backend API
        await callPurchaseAPI();
        
        // Show success message
        Swal.fire({
          icon: 'success',
          title: 'Purchase Successful!',
          text: `Successfully purchased ${purchaseAmount}kg of ${credit.name}`,
          footer: `<small>Transaction Hash: 0x${generateFakeHash()}</small>`
        });
        
        // Notify parent component
        if (onPurchaseSuccess) {
          onPurchaseSuccess();
        }
      }
    } catch (error) {
      console.error('Purchase error:', error);
      Swal.fire({
        icon: 'error',
        title: 'Purchase Failed',
        text: 'Failed to complete the purchase. Please try again.',
      });
    } finally {
      setIsPurchasing(false);
    }
  };

  const simulateTransaction = async (totalCost) => {
    // Simulate MetaMask transaction popup
    return new Promise((resolve) => {
      setTimeout(() => {
        console.log(`Simulating transaction: ${totalCost} ETH`);
        resolve();
      }, 2000);
    });
  };

  const callPurchaseAPI = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/buyer/purchase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          creditId: credit.id,
          buyerAddress: account,
          amount: purchaseAmount,
          price: credit.price,
        }),
      });
      
      const result = await response.json();
      console.log('Purchase API response:', result);
    } catch (error) {
      console.error('API call failed:', error);
    }
  };

  const generateFakeHash = () => {
    return Math.random().toString(16).substring(2, 66).padEnd(64, '0');
  };

  const formatAddress = (address) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  const getNetworkBadgeColor = () => {
    switch (network) {
      case 'Sepolia':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'Wrong Network':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Purchase Hydrogen Credit</h3>
        <p className="text-sm text-gray-600">Connect your MetaMask wallet to purchase this credit</p>
      </div>

      {/* Wallet Connection Status */}
      <div className="mb-6">
        {!isConnected ? (
          <button
            onClick={connectWallet}
            disabled={isConnecting}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
          >
            {isConnecting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Connecting...
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                </svg>
                Connect MetaMask
              </>
            )}
          </button>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">Wallet Address:</span>
              <span className="text-sm font-mono text-gray-900">{formatAddress(account)}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">Network:</span>
              <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getNetworkBadgeColor()}`}>
                {network}
              </span>
            </div>
            {network !== 'Sepolia' && (
              <button
                onClick={switchToSepolia}
                className="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
              >
                Switch to Sepolia
              </button>
            )}
          </div>
        )}
      </div>

      {/* Purchase Form */}
      {isConnected && network === 'Sepolia' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Purchase Amount (kg)
            </label>
            <input
              type="number"
              min="1"
              max={credit.amount}
              value={purchaseAmount}
              onChange={(e) => setPurchaseAmount(parseInt(e.target.value) || 1)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              Available: {credit.amount} kg • Price: {credit.price} ETH/kg
            </p>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-green-800">Total Cost:</span>
              <span className="text-lg font-bold text-green-900">
                {(purchaseAmount * credit.price).toFixed(4)} ETH
              </span>
            </div>
          </div>

          <button
            onClick={purchaseCredit}
            disabled={isPurchasing}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
          >
            {isPurchasing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Processing Purchase...
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m6 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
                </svg>
                Purchase Credit
              </>
            )}
          </button>
        </div>
      )}

      {/* Info Box */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div className="text-sm text-blue-800">
            <p className="font-medium">Sepolia Testnet</p>
            <p className="mt-1">This is a test network. You'll need Sepolia ETH to make purchases. Get free test ETH from a Sepolia faucet.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetaMaskBuyer;
