# Moorea Privacy Policy

**Last Updated: October 6, 2025**

## Introduction

Welcome to Moorea ("we," "our," or "us"). This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI-powered moodboard generation service (the "Service"). Please read this privacy policy carefully. If you do not agree with the terms of this privacy policy, please do not access the Service.

## 1. Information We Collect

### 1.1 Personal Information You Provide
When you create an account or use our Service, we may collect:
- **Account Information**: Username, email address, and password (stored as a secure hash)
- **Profile Data**: Optional profile information you choose to provide
- **Moodboard Content**: Titles, descriptions, and aesthetic preferences for saved moodboards

### 1.2 Automatically Collected Information
- **Usage Data**: Information about how you use the Service, including pages visited, features used, and time spent
- **Device Information**: Device type, operating system, browser type, and IP address
- **Session Data**: Authentication tokens and session identifiers for maintaining your login state

### 1.3 Images and Content
- **Uploaded Images**: When you upload clothing images for moodboard generation:
  - Images are processed temporarily in-memory for AI analysis
  - Images are **not permanently stored** on our servers unless you explicitly save them to your account
  - When you save a moodboard, only image URLs and metadata are stored, not the actual image files
- **Generated Moodboards**: When you save a moodboard, we store:
  - The aesthetic classification detected by our AI
  - URLs to images from third-party sources (Unsplash, Pexels, Flickr, Pinterest)
  - Image metadata including photographer credits and source information

### 1.4 Pinterest API Data
When using Pinterest integration, we access the following Pinterest API endpoints:
- **Pins API**: To search and retrieve Pinterest pins based on aesthetic keywords
- **Boards API**: To access public board information for attribution
- **User API**: To retrieve public user information for photographer credits

**Data Retrieved from Pinterest API:**
- Pin URLs and image URLs (publicly accessible)
- Pin descriptions and titles (public content)
- Board names and descriptions (public information)
- User display names (public profile information)
- Pin creation dates and engagement metrics (public data)

**Data NOT Retrieved:**
- Private pins or boards
- User email addresses or personal contact information
- Pinterest login credentials or session data
- Private user preferences or settings

## 2. How We Use Your Information

We use the information we collect to:

### 2.1 Provide and Improve Service
- Generate AI-powered aesthetic moodboards based on your uploaded images
- Classify fashion aesthetics using machine learning (CLIP model)
- Search and curate images from third-party APIs (Unsplash, Pexels, Flickr, Pinterest)
- Save and manage your moodboard collections
- Authenticate and maintain your user account
- Optimize performance through caching of aesthetic classifications

### 2.2 Communication
- Send service-related notifications about your account or moodboards
- Respond to your inquiries and provide customer support
- Send updates about new features or changes to our Service (with your consent)

### 2.3 Analytics and Improvement
- Analyze usage patterns to improve our Service
- Monitor Service performance and optimize response times
- Develop new features and aesthetic categories

### 2.4 Legal Compliance
- Comply with legal obligations and regulations
- Protect the rights, property, and safety of Moorea, our users, and the public
- Enforce our Terms of Service

## 3. Third-Party Content Sources and APIs

### 3.1 Data Processing Infrastructure
We use the following third-party services to process and store your data:

**Cloud Infrastructure Providers:**
- **PostgreSQL Database**: Stores your account information and saved moodboards
- **Redis Cache**: Temporarily caches API responses and AI classifications for performance
- **Cloud Storage**: Stores application data and backups

**AI/ML Services:**
- **CLIP Model**: Processes uploaded images for aesthetic classification
- **OpenAI Services**: May be used for enhanced AI features (if implemented)

All third-party processors are bound by data processing agreements that require them to:
- Process data only as instructed by Moorea
- Implement appropriate security measures
- Not use data for their own purposes
- Delete data when no longer needed

### 3.2 Image Source APIs
We integrate with the following third-party services to provide moodboard content:

#### Unsplash
- **Purpose**: Primary source for high-quality lifestyle photography
- **Data Accessed**: Public image URLs, photographer names, download tracking URLs
- **Data Shared**: Search queries based on detected aesthetics
- **Storage**: We cache image URLs and metadata; we do **not** store actual images
- **Attribution**: Full photographer credit displayed in all moodboards
- **Compliance**: We trigger download events as required by Unsplash API terms

#### Pexels
- **Purpose**: Secondary content source for fashion and lifestyle images
- **Data Accessed**: Public image URLs, photographer names
- **Data Shared**: Search queries based on detected aesthetics
- **Storage**: Image URLs and photographer credits only
- **Attribution**: Photographer credit provided where applicable

#### Flickr
- **Purpose**: Additional content source for diverse aesthetic imagery
- **Data Accessed**: Public Creative Commons licensed images, photographer names
- **Data Shared**: Search queries based on detected aesthetics
- **Storage**: Image URLs and metadata only
- **License Compliance**: Only Creative Commons and public domain images (licenses 4-10)

#### Pinterest (Planned Integration)
- **Purpose**: Enhanced content diversity from user-curated boards
- **Data Accessed**: Public pin URLs, user names, board information
- **Data Shared**: Search queries based on detected aesthetics
- **Storage**: Pin URLs and attribution information only
- **Compliance**: Full Pinterest user and source attribution in moodboards

### 3.2 Important Limitations on Third-Party Data
We **strictly prohibit** the following uses of third-party API data:
- ❌ Storing images or content beyond URLs and metadata
- ❌ Using content for training AI models (our CLIP model is pre-trained)
- ❌ Combining your data with third-party data for advertising purposes
- ❌ Sharing or selling API data to third parties
- ❌ Using content outside the moodboard generation context
- ❌ Targeting you with advertising on other platforms
- ❌ Bundling or reselling content through data brokers

## 4. Data Storage and Security

### 4.1 Security Measures
We implement industry-standard security measures to protect your information:
- **Password Security**: bcrypt hashing with unique salts for all passwords (industry best practice)
- **Authentication**: JWT (JSON Web Token) based session management with 30-minute expiry
- **Data Encryption**: HTTPS encryption for all data transmission
- **Database Security**: PostgreSQL with proper access controls and authentication
- **API Security**: Secure credential storage and access token management

### 4.2 Data Retention
- **Uploaded Images**: Processed temporarily in-memory only; **not permanently stored**
- **User Accounts**: Retained until you request account deletion
- **Saved Moodboards**: Retained until you delete them or close your account
- **Cache Data**: Aesthetic classification results cached for performance (up to 24 hours)
- **Session Tokens**: Expire after 30 minutes of inactivity

### 4.3 Data Location
- **Database**: PostgreSQL database hosted on secure servers
- **Processing**: Image analysis performed server-side with no persistent storage
- **Third-Party Content**: Images remain hosted by source providers (Unsplash, Pexels, Flickr, Pinterest)

## 5. Data Sharing and Disclosure

### 5.1 We Do NOT Share Your Personal Data
We do **not** sell, rent, or share your personal information with third parties for their marketing purposes.

### 5.2 Limited Sharing Circumstances
We may share information only in these specific circumstances:
- **With Your Consent**: When you explicitly authorize us to share information
- **Service Providers**: With trusted third-party APIs (Unsplash, Pexels, Flickr, Pinterest) only for moodboard generation
- **Legal Requirements**: When required by law, subpoena, or court order
- **Safety and Security**: To protect the rights, property, or safety of Moorea, our users, or the public
- **Business Transfers**: In connection with a merger, acquisition, or sale of assets (you will be notified)

### 5.3 What We Share with Third-Party APIs
When generating moodboards, we share only:
- Search queries derived from AI-detected aesthetics (e.g., "minimalist fashion," "cottagecore")
- **We do NOT share**: Your personal information, email, username, or original uploaded images

## 6. Your Rights and Choices

### 6.1 Account Management
- **Access**: View your account information and saved moodboards at any time
- **Update**: Modify your username, email, or account details
- **Delete**: Request complete account deletion with all associated data
- **Export**: Request a copy of your saved moodboard data

### 6.2 Data Control
- **Opt-Out of Communications**: Unsubscribe from promotional emails (service emails still required)
- **Moodboard Management**: Delete individual moodboards at any time
- **Session Control**: Log out to terminate your session and invalidate tokens

### 6.3 Regional Privacy Rights

#### GDPR (European Users)
If you are in the European Economic Area, you have the right to:
- Access, correct, or delete your personal data
- Object to or restrict processing of your data
- Data portability
- Withdraw consent at any time
- Lodge a complaint with your data protection authority

#### CCPA (California Users)
If you are a California resident, you have the right to:
- Know what personal information we collect, use, and share
- Request deletion of your personal information
- Opt-out of the sale of personal information (we don't sell data)
- Non-discrimination for exercising your privacy rights

To exercise these rights, contact us at: annaszilviakennedy@gmail.com

## 7. Children's Privacy

Our Service is **not intended for children under 13 years of age**. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has provided us with personal information, please contact us immediately, and we will delete such information.

## 8. Cookies and Tracking Technologies

### 8.1 Cookies We Use
- **Essential Cookies**: Required for authentication and session management
- **Performance Cookies**: Help us understand how you use the Service
- **Cache Management**: Redis caching for improved performance (no personal data)

### 8.2 Third-Party Tracking
We do **not** use third-party advertising or tracking cookies. Any tracking is limited to essential Service functionality.

## 9. Content Attribution and Intellectual Property

### 9.1 Photographer Attribution
- All moodboards display full photographer credits from source APIs
- Links to original content sources (Unsplash, Pexels, Flickr, Pinterest) provided
- Content used respectfully within moodboard generation context only

### 9.2 Your Rights to Generated Moodboards
- You own the moodboard collections you create and save
- Moodboards are for personal use and inspiration
- Individual images remain the property of their respective creators
- You must respect the licenses and terms of source platforms when sharing moodboards

### 9.3 Our Use of AI and Machine Learning
- **CLIP Model**: Our pre-trained CLIP model analyzes uploaded images for aesthetic classification
- **Pinterest Data Processing**: Pinterest images are processed through our AI system to:
  - Match aesthetic preferences with relevant Pinterest content
  - Generate similarity scores for moodboard curation
  - Classify Pinterest content for better search results
- **No Training on User Data**: We do **not** use your uploaded images or Pinterest data to train or improve our AI models
- **Derivative Works**: Pinterest content is used only for moodboard generation and aesthetic matching
- **AI Transparency**: All AI processing is for the stated purpose of moodboard generation only

### 9.4 User Controls and Opt-Out Options
You have the following controls over Pinterest data processing:
- **Disable Pinterest Integration**: You can opt-out of Pinterest content in your moodboards
- **Data Processing Preferences**: Control how your data is used for AI analysis
- **Content Filtering**: Choose which types of Pinterest content to include
- **Account Deletion**: Complete removal of all Pinterest-related data upon account deletion

To modify these preferences, contact us at: annaszilviakennedy@gmail.com

## 10. International Data Transfers

### 10.1 Cross-Border Data Processing
If you access the Service from outside the United States, your information may be transferred to, stored, and processed in the United States or other countries where we or our service providers operate. These countries may have different data protection laws than your country of residence.

### 10.2 Data Transfer Safeguards
We ensure appropriate safeguards for international data transfers through:
- **Standard Contractual Clauses (SCCs)**: Used for transfers to countries without adequacy decisions
- **Adequacy Decisions**: We prioritize transfers to countries with EU adequacy decisions
- **Data Processing Agreements**: All third-party processors are bound by appropriate contractual safeguards
- **Technical Safeguards**: Encryption in transit and at rest for all data transfers

### 10.3 Pinterest API Data Transfers
When using Pinterest integration:
- Pinterest data is processed in accordance with Pinterest's data processing terms
- We do not transfer Pinterest data to countries without appropriate safeguards
- Pinterest data is subject to the same transfer protections as your personal data

### 10.4 Your Rights Regarding Transfers
You have the right to:
- Know which countries your data is transferred to
- Request information about the safeguards in place
- Withdraw consent for transfers (though this may limit Service functionality)

## 11. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. We will notify you of any changes by:
- Updating the "Last Updated" date at the top of this policy
- Sending you an email notification for material changes
- Displaying a prominent notice on our Service

Your continued use of the Service after changes constitutes acceptance of the updated Privacy Policy.

## 12. Data Breach Notification

In the event of a data breach that may compromise your personal information, we will:
- Notify affected users within 72 hours of discovering the breach
- Describe the nature of the breach and data affected
- Provide steps you can take to protect yourself
- Report to relevant authorities as required by law

## 13. Third-Party Links

Our Service may contain links to third-party websites or services (such as photographer profiles on Unsplash or Pinterest). We are not responsible for the privacy practices of these third parties. We encourage you to review their privacy policies before providing any personal information.

## 14. Developer Guidelines Compliance

### 14.1 Transparency Commitment
We are committed to being honest and transparent about:
- What data we collect and how we use it
- Which third-party services we integrate with
- How your moodboards are generated and stored

### 14.2 API Data Handling
We comply with all developer guidelines from our API providers:
- **No Unauthorized Actions**: We never take actions on your behalf without your explicit knowledge and consent
- **No Automation Abuse**: All moodboard generation requires deliberate user action
- **No Data Bundling**: We do not combine API data with other advertising services
- **Respect for Rate Limits**: We implement caching and rate limiting to respect API provider limits
- **No Competitor Research**: We do not use API data for platform benchmarking or competitor analysis

## 15. User Conduct and Restrictions

By using our Service, you agree **not** to:
- Upload inappropriate, offensive, or illegal content
- Attempt to reverse engineer our AI models or Service
- Violate any third-party API terms of service
- Use automated tools to generate moodboards at scale
- Share or resell moodboard content for commercial purposes without proper attribution
- Circumvent any security measures or rate limiting

## 16. Contact Us

If you have questions about this Privacy Policy or our data practices, please contact us at:

**Email**: annaszilviakennedy@gmail.com  
**Website**: Moorea.mood.com  
**GitHub**: https://github.com/kovta/moorea  
**Response Time**: We aim to respond to privacy inquiries within 7 business days

## 17. Specific API Provider Compliance

### 17.1 Pinterest Developer Guidelines Compliance
We comply with Pinterest's Developer Guidelines by:
✅ Being honest and transparent about our Service functionality  
✅ Not storing information accessed through Pinterest API (only URLs)  
✅ Only accessing public Pinterest content  
✅ Not soliciting or collecting login credentials  
✅ Keeping API credentials private and secure  
✅ Not evading policy enforcement systems  
✅ Following all technical documentation  
✅ Maintaining this privacy policy consistent with applicable laws  

**What We Do with Pinterest Content:**
- Use pins as content sources for moodboards (like Unsplash/Pexels)
- Provide full Pinterest user attribution
- Link pins back to their source on Pinterest
- Not cover or obscure Pinterest content

**What We Do NOT Do:**
- Take actions on behalf of Pinterest users without consent
- Offer automated features that lessen authenticity
- Attempt platform insights or competitor research
- Use scraping or unauthorized data extraction
- Misrepresent our relationship with Pinterest
- Use Pinterest data for advertising outside Pinterest
- Bundle or sell Pinterest content/data
- Require or incentivize engagement
- Target children under 13

### 17.2 Unsplash API Compliance
✅ Trigger download events as required  
✅ Display photographer attribution  
✅ Link to original Unsplash pages  
✅ Respect rate limits with caching  

### 17.3 Pexels API Compliance
✅ Display photographer credits where applicable  
✅ Use within free tier rate limits  
✅ Link to original content sources  

### 17.4 Flickr API Compliance
✅ Only use Creative Commons licensed content  
✅ Display photographer attribution  
✅ Respect API rate limits  

---

## Summary - Your Privacy at a Glance

🔒 **Your images are never permanently stored** - processed temporarily only  
🚫 **We never sell your data** - period  
✅ **You control your moodboards** - save, edit, or delete anytime  
🎨 **Third-party content properly attributed** - full photographer credits  
🔐 **Secure authentication** - JWT tokens and hashed passwords  
🌐 **Transparent API usage** - clear disclosure of all integrations  
👤 **Your rights respected** - access, export, or delete your data anytime  
🛡️ **No tracking or advertising** - we don't use ad networks or sell to brokers  

---

Thank you for trusting Moorea with your creative inspiration journey. We are committed to protecting your privacy while helping you discover beautiful aesthetic moodboards.
