# GraphLinq Telegram Bot

![GraphLinq Logo](https://cdn.prod.website-files.com/65de56ee9ed70741bfc4efc6/65e64c7d4bcddb3fadcd943b_glq_faviconn.png)

A comprehensive Telegram bot for the GraphLinq ecosystem that provides staking information, price data, and community resources for GLQ token holders.

## 🔗 Bot Access

**Live Bot**: [@GraphlinqBot](https://t.me/GraphlinqBot)

## ✨ Features

### 🔐 Private Commands (DM only)
- **Address Management**: Set and view your wallet address
- **Personal Staking Info**: View your staked GLQ, rewards, tier, and rank
- **Portfolio Tracking**: Monitor your staking position and USD value

### 🌐 Public Commands
- **Network Statistics**: Total stakers, total staked, APY rates
- **Tier Information**: View staking tiers and their distributions  
- **Price Data**: Real-time GLQ pricing and market data
- **Community Resources**: Links to websites, social media, exchanges
- **Documentation**: Quick access to GraphLinq resources

### 🔧 Administrative Features
- **Maintenance Mode**: Bot-wide maintenance with admin bypass
- **System Monitoring**: Server stats, uptime, and performance metrics
- **Advanced Logging**: Multi-level logging system with file separation

## 🚀 Quick Start

### Prerequisites
- **Python 3.6-3.10** (3.7+ recommended)
  > ⚠️ **Important**: This project uses `python-telegram-bot==13.0` which is incompatible with Python 3.11+ and does not support the async patterns introduced in v20+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Ethereum/Web3 RPC endpoint (Infura, Alchemy, etc.)
- LiveCoinWatch API key (optional, for price data)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jrbgit/GraphLinq.TelegramBot.git
   cd GraphLinq.TelegramBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Required
   TELEGRAM_KEY=your_telegram_bot_token_here
   NETWORK_URL=https://your-ethereum-rpc-endpoint.com
   CONTRACT_ADDRESS=0x9F9c8ec3534c3cE16F928381372BfbFBFb9F4D24
   
   # Optional
   LCW_API_KEY=your_livecoinwatch_api_key
   MAINT_MODE=0
   ALLOWED_ADMIN=your_telegram_user_id
   ```

4. **Run the bot**
   ```bash
   python3 bot.py
   ```

### Docker Deployment

1. **Using Docker Compose** (Recommended)
   ```bash
   docker-compose up -d
   ```

2. **Manual Docker Build**
   ```bash
   docker build -t graphlinq-bot .
   docker run -d --name graphlinq-bot graphlinq-bot
   ```

## 📋 Command Reference

### Private Commands (Direct Message Required)

| Command | Description | Example |
|---------|-------------|---------|
| `/setmyaddress <address>` | Set your wallet address | `/setmyaddress 0x123...` |
| `/myaddress` | View your stored address | `/myaddress` |
| `/mytotal` | View your total staked GLQ | `/mytotal` |
| `/myrank` | View your staking rank | `/myrank` |
| `/mytier` | View your current tier | `/mytier` |
| `/myrewards` | View claimable rewards | `/myrewards` |

### Public Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and bot info |
| `/help` | Display command help menu |
| `/apy` | Current APY rates for each tier |
| `/tiers` | GLQ staked in each tier |
| `/totalstaked` | Total GLQ staked across all tiers |
| `/totalstakers` | Number of active stakers |
| `/supply` | GraphLinq Chain supply information |
| `/websites` | Official GraphLinq websites |
| `/socials` | Social media links |
| `/staking` | Staking guide and resources |
| `/documentation` | Link to official docs |
| `/listings` | Where to buy/trade GLQ |
| `/status` | Network status links |
| `/shortcuts` | Command aliases |

### Legacy Aliases
For backward compatibility, the following shortcuts are supported:
- `/set` → `/setmyaddress`
- `/address` → `/myaddress` 
- `/total` → `/mytotal`
- `/rank` → `/myrank`
- `/tier` → `/mytier`
- `/rewards` → `/myrewards`
- `/staked` → `/totalstaked`
- `/stakers` → `/totalstakers`

## 🏗️ Architecture

### File Structure
```
GraphLinq.TelegramBot/
├── bot.py                 # Main bot application
├── config_base.py         # Base configuration and API keys
├── config_contract.py     # Smart contract interface
├── config_logging.py      # Logging configuration
├── config_maint.py        # Maintenance mode settings
├── config_msgs.py         # Bot messages and responses
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker deployment
├── Dockerfile            # Docker container config
├── .env                  # Environment variables (create this)
└── logs/                 # Log files directory
    ├── debug.log
    ├── info.log
    ├── warning.log
    ├── error.log
    └── critical.log
```

### Key Components

1. **Smart Contract Integration**: Direct interaction with GraphLinq staking contract
2. **Database**: SQLite for user address storage
3. **Price APIs**: LiveCoinWatch and GraphLinq Hub integration
4. **Logging System**: Multi-level logging with file separation
5. **Maintenance Mode**: System-wide maintenance with admin bypass

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TELEGRAM_KEY` | ✅ | Bot token from BotFather | `123456:ABC-DEF...` |
| `NETWORK_URL` | ✅ | Ethereum RPC endpoint | `https://mainnet.infura.io/v3/...` |
| `CONTRACT_ADDRESS` | ✅ | GraphLinq staking contract | `0x9F9c8ec3534c3cE16F928381372BfbFBFb9F4D24` |
| `LCW_API_KEY` | ❌ | LiveCoinWatch API key | `abc123...` |
| `MAINT_MODE` | ❌ | Maintenance mode (0=off, 1=on) | `0` |
| `ALLOWED_ADMIN` | ❌ | Admin Telegram user ID | `123456789` |

### Smart Contract ABI

The bot includes the complete ABI for the GraphLinq staking contract, supporting functions like:
- `getDepositedGLQ()` - User staked amount
- `getGlqToClaim()` - Claimable rewards  
- `getPosition()` - User rank
- `getWalletCurrentTier()` - User tier
- `getTiersAPY()` - Current APY rates
- `getTotalStakers()` - Total staker count

## 📊 Data Sources

- **Staking Data**: Direct smart contract queries via Web3
- **Price Data**: LiveCoinWatch API and GraphLinq Hub API
- **Supply Data**: GraphLinq Chain Explorer API
- **User Data**: Local SQLite database for address storage

## 🔒 Privacy & Security

- **Address Storage**: User addresses stored locally in encrypted SQLite database
- **Private Commands**: Restricted to direct messages only
- **Admin Controls**: Maintenance mode with admin bypass functionality
- **API Key Masking**: Sensitive data masked in logs
- **Error Handling**: Comprehensive exception handling and logging

## 🚨 Maintenance Mode

The bot supports maintenance mode for updates and troubleshooting:

1. **Enable**: Set `MAINT_MODE=1` in environment
2. **Admin Bypass**: Admin users can still access all functions
3. **User Message**: Automatic maintenance message to regular users
4. **Logging**: All maintenance events logged

## 📝 Logging

The bot implements a comprehensive logging system:

- **debug.log**: Detailed execution flow
- **info.log**: General information and startup
- **warning.log**: Non-critical issues
- **error.log**: Error conditions
- **critical.log**: Critical failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/jrbgit/GraphLinq.TelegramBot/issues)
- **GraphLinq Discord**: [Join Community](https://discord.com/invite/tCCas5sCWA)
- **Documentation**: [GraphLinq Docs](https://docs.graphlinq.io)

## 🔗 Related Links

- **GraphLinq Protocol**: [https://graphlinq.io](https://graphlinq.io)
- **Staking Platform**: [https://app.graphlinq.io/app/staking](https://app.graphlinq.io/app/staking)
- **Explorer**: [https://explorer.graphlinq.io](https://explorer.graphlinq.io)
- **Hub**: [https://hub.graphlinq.io](https://hub.graphlinq.io)

## 👨‍💻 Developer

**Author**: jrbgit  
**Contact**: [@jr00t_GLQ](https://twitter.com/jr00t_GLQ)  
**Website**: [jr00t.com](https://jr00t.com)

---

*Built with ❤️ for the GraphLinq community*