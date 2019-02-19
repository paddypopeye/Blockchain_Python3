new Vue({
    el: '#app',
    data: {
        blockchain: [
            {
                previous_hash: 'fawsqwar2', index: 0, transactions: [
                    {
                        sender: 'fsdf23',
                        recipient: 'fadwfs314',
                        amount: 5.5
                    },
                    {
                        sender: 'fssfsddf23',
                        recipient: 'fadewasfwfs314',
                        amount: 15.5
                    }
                ]
            },
            {
                previous_hash: 'awdsf14', index: 1, transactions: [
                    {
                        sender: 'afe',
                        recipient: 'fadwe322fs314',
                        amount: 1.5
                    },
                    {
                        sender: 'fssddf23',
                        recipient: 'fadesfwfs314',
                        amount: 4.5
                    }
                ]
            }
        ],
        openTransactions: [
            {
                sender: '23r32r3fsas',
                recipient: 'feadsf25',
                amount: 5.9
            },
            {
                sender: '23r23r2ra3fsas',
                recipient: 'sdfsfa',
                amount: 1.5
            }
        ],
        wallet: null,
        view: 'chain',
        walletLoading: false,
        txLoading: false,
        dataLoading: false,
        showElement: null,
        error: null,
        success: null,
        funds: 0,
        outgoingTx: {
            recipient: '',
            amount: 0
        }
    },
    computed: {
        loadedData: function () {
            if (this.view === 'chain') {
                return this.blockchain;
            } else {
                return this.openTransactions
            }
        }
    },
    methods: {
        onCreateWallet: function () {
            // Send Http request to create a new wallet (and return keys)
            if (Math.random() > 0.5) {
                this.error = null
                this.success = 'Successfully stored transaction!';
                this.wallet = { private_key: 'fsde2523tfasg234twfg24qafew', public_key: '532fsdarf23rf' };
            } else {
                this.success = null;
                this.error = 'Something went wrong!';
                this.wallet = null;
            }
        },
        onLoadWallet: function () {
            // Send Http request to load an existing wallet (from a file on the server)
            if (Math.random() > 0.5) {
                this.error = null
                this.success = 'Successfully stored transaction!';
                this.wallet = { private_key: 'fsde2523tfasg234twfg24qafew', public_key: '532fsdarf23rf' };
            } else {
                this.success = null;
                this.error = 'Something went wrong!';
                this.wallet = null;
            }
        },
        onSendTx: function () {
            // Send Transaction to backend
            if (Math.random() > 0.5) {
                this.error = null
                this.success = 'Successfully stored transaction!'
                this.funds = this.funds - this.outgoingTx.amount
            } else {
                this.success = null;
                this.error = 'Something went wrong!'
            }
        },
        onMine: function() {
            if (Math.random() > 0.5) {
                this.error = null
                this.success = 'Successfully mined coins!'
                this.funds = this.funds + 10
            } else {
                this.success = null;
                this.error = 'Something went wrong!'
            }
        },
        onLoadData: function () {
            if (this.view === 'chain') {
                // Load blockchain data
                if (Math.random() > 0.5) {
                    this.error = null
                } else {
                    this.success = null;
                    this.error = 'Something went wrong!'
                }
            } else {
                // Load transaction data
                if (Math.random() > 0.5) {
                    this.error = null
                } else {
                    this.success = null;
                    this.error = 'Something went wrong!'
                }
            }
        }
    }
})
