import React from 'react';
import { Link } from 'react-router-dom';

const PrivacyPolicy: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-lg p-8 md:p-12">
          <div className="mb-8">
            <Link
              to="/"
              className="text-purple-600 hover:text-purple-800 inline-flex items-center gap-2 mb-6 text-lg"
            >
              <span>←</span>
              Back to Home
            </Link>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Privacy Policy
            </h1>
            <p className="text-gray-600 text-sm mb-8">
              Effective Date: January 1, 2025 | Last Updated: January 1, 2025
            </p>
          </div>

          <div className="prose prose-lg prose-gray max-w-none space-y-8">
            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Introduction</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                Moodboard Generator ("we," "our," or "us") is committed to protecting your privacy and personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI-powered moodboard generation service.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                By using our service, you consent to the data practices described in this Privacy Policy. If you do not agree with the terms of this Privacy Policy, please do not use our service.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Information We Collect</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">1. Image Data</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Uploaded Images</strong>: When you upload clothing images to generate moodboards, we temporarily process these images using our AI classification system</li>
                    <li><strong>Processing Purpose</strong>: Images are analyzed to identify fashion aesthetics and generate personalized moodboards</li>
                    <li><strong>Storage Duration</strong>: Images are processed in-memory only and are not permanently stored on our servers</li>
                    <li><strong>Consent Required</strong>: By uploading an image, you explicitly consent to our processing of your image for moodboard generation purposes</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">2. User Account Information (Optional)</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Registration Data</strong>: Username, email address, and encrypted password (if you choose to create an account)</li>
                    <li><strong>Authentication</strong>: Secure JWT-based authentication with SHA256 password hashing</li>
                    <li><strong>Purpose</strong>: Account creation is optional and only required for saving moodboards to your personal collection</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">3. Usage Data</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Aesthetic Preferences</strong>: Anonymized data about which fashion aesthetics you're interested in</li>
                    <li><strong>Moodboard History</strong>: Saved moodboards and their associated aesthetic classifications (if you have an account)</li>
                    <li><strong>Performance Metrics</strong>: Aggregated, anonymized usage statistics to improve our service</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">4. Technical Data</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Device Information</strong>: Browser type, operating system, IP address (anonymized)</li>
                    <li><strong>Usage Analytics</strong>: Page views, feature usage, and performance metrics</li>
                    <li><strong>Error Logs</strong>: Technical error information to improve service reliability</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">How We Use Your Information</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Primary Uses</h3>
                  <ol className="list-decimal list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Moodboard Generation</strong>: Process uploaded images to create personalized aesthetic moodboards</li>
                    <li><strong>AI Classification</strong>: Use CLIP (Contrastive Language-Image Pre-training) model to analyze fashion aesthetics</li>
                    <li><strong>Content Curation</strong>: Generate relevant lifestyle images and style recommendations</li>
                    <li><strong>Service Improvement</strong>: Analyze usage patterns to enhance our AI models and user experience</li>
                  </ol>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Secondary Uses</h3>
                  <ol className="list-decimal list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Account Management</strong>: Provide user authentication and moodboard saving functionality</li>
                    <li><strong>Customer Support</strong>: Respond to inquiries and provide technical assistance</li>
                    <li><strong>Legal Compliance</strong>: Meet legal obligations and protect our rights</li>
                    <li><strong>Service Analytics</strong>: Understand usage patterns and improve our platform</li>
                  </ol>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Third-Party API Integrations</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Content Sources</h3>
                  <p className="text-gray-700 leading-relaxed text-lg">
                    We integrate with the following third-party APIs to provide high-quality moodboard content:
                  </p>

                  <div className="space-y-4 mt-4">
                    <div>
                      <h4 className="text-xl font-semibold text-gray-800 mb-2">Unsplash API</h4>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 ml-6 text-lg">
                        <li><strong>Purpose</strong>: Primary source for lifestyle photography and fashion imagery</li>
                        <li><strong>Data Shared</strong>: Search keywords and aesthetic terms (no personal images)</li>
                        <li><strong>Attribution</strong>: Full photographer credits displayed in moodboards</li>
                        <li><strong>Privacy</strong>: Unsplash's privacy policy applies to their service</li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="text-xl font-semibold text-gray-800 mb-2">Pexels API</h4>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 ml-6 text-lg">
                        <li><strong>Purpose</strong>: Secondary content source for fashion photography and lifestyle images</li>
                        <li><strong>Data Shared</strong>: Search keywords and aesthetic terms (no personal images)</li>
                        <li><strong>Attribution</strong>: Photographer credits provided where applicable</li>
                        <li><strong>Privacy</strong>: Pexels' privacy policy applies to their service</li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="text-xl font-semibold text-gray-800 mb-2">Pinterest API (Future Integration)</h4>
                      <ul className="list-disc list-inside text-gray-700 space-y-1 ml-6 text-lg">
                        <li><strong>Purpose</strong>: Enhanced content diversity for moodboard generation</li>
                        <li><strong>Data Shared</strong>: Search keywords and aesthetic terms (no personal images)</li>
                        <li><strong>Attribution</strong>: Full Pinterest user and original source attribution</li>
                        <li><strong>Privacy</strong>: Pinterest's privacy policy applies to their service</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">AI/ML Services</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Hugging Face</strong>: CLIP model inference for image classification</li>
                    <li><strong>Data Shared</strong>: Image embeddings and aesthetic vocabulary (no personal identifiers)</li>
                    <li><strong>Purpose</strong>: Fashion aesthetic classification and similarity matching</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Data Security and Protection</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Security Measures</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Encryption</strong>: All data transmission uses HTTPS/TLS encryption</li>
                    <li><strong>Authentication</strong>: Secure JWT-based authentication with SHA256 password hashing</li>
                    <li><strong>Access Controls</strong>: Limited access to personal data on a need-to-know basis</li>
                    <li><strong>Regular Audits</strong>: Periodic security assessments and vulnerability testing</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Data Retention</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Uploaded Images</strong>: Processed temporarily and immediately deleted after moodboard generation</li>
                    <li><strong>User Accounts</strong>: Retained until account deletion or 2 years of inactivity</li>
                    <li><strong>Usage Analytics</strong>: Aggregated data retained for up to 3 years for service improvement</li>
                    <li><strong>Moodboard Collections</strong>: Retained until user account deletion</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Your Rights and Choices</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Access and Control</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Account Deletion</strong>: You can delete your account and all associated data at any time</li>
                    <li><strong>Data Export</strong>: Request a copy of your personal data in a portable format</li>
                    <li><strong>Data Correction</strong>: Update or correct your account information</li>
                    <li><strong>Opt-Out</strong>: Unsubscribe from communications or disable analytics tracking</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Image Processing Consent</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Explicit Consent</strong>: By uploading an image, you grant us permission to process it for moodboard generation</li>
                    <li><strong>Withdrawal</strong>: You can withdraw consent by deleting uploaded images or your account</li>
                    <li><strong>Purpose Limitation</strong>: Images are only processed for the stated purpose of moodboard generation</li>
                    <li><strong>No Commercial Use</strong>: We do not use your images for commercial purposes beyond service provision</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Communication Preferences</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Email Notifications</strong>: Opt-in for account-related notifications and service updates</li>
                    <li><strong>Marketing Communications</strong>: Opt-in for promotional content and feature announcements</li>
                    <li><strong>Service Updates</strong>: Essential service notifications (cannot be opted out)</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">International Data Transfers</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Data Processing Locations</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Primary Processing</strong>: United States (AWS cloud infrastructure)</li>
                    <li><strong>Third-Party Services</strong>: Data may be processed by our API partners globally</li>
                    <li><strong>Adequacy Decisions</strong>: We ensure appropriate safeguards for international transfers</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Compliance Frameworks</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>GDPR</strong>: European Union General Data Protection Regulation compliance</li>
                    <li><strong>CCPA</strong>: California Consumer Privacy Act compliance</li>
                    <li><strong>PIPEDA</strong>: Personal Information Protection and Electronic Documents Act (Canada)</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Children's Privacy</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                Our service is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has provided us with personal information, please contact us to have the information removed.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Cookies and Tracking Technologies</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Types of Cookies</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Essential Cookies</strong>: Required for basic service functionality and authentication</li>
                    <li><strong>Analytics Cookies</strong>: Help us understand usage patterns and improve our service</li>
                    <li><strong>Preference Cookies</strong>: Remember your settings and preferences</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Cookie Management</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Browser Settings</strong>: You can control cookies through your browser settings</li>
                    <li><strong>Opt-Out</strong>: Disable non-essential cookies while maintaining service functionality</li>
                    <li><strong>Third-Party Tracking</strong>: We do not use third-party advertising or tracking cookies</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Changes to This Privacy Policy</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Notification Process</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Material Changes</strong>: We will notify users of significant changes via email or service notification</li>
                    <li><strong>Regular Updates</strong>: Minor updates will be posted on this page with updated "Last Updated" date</li>
                    <li><strong>Continued Use</strong>: Continued use of our service after changes constitutes acceptance of the updated policy</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Version History</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Version 1.0</strong>: Initial privacy policy (January 1, 2025)</li>
                    <li><strong>Future Versions</strong>: Will be documented with change summaries</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Legal Basis for Processing (GDPR)</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Lawful Bases</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Consent</strong>: Explicit consent for image processing and optional account creation</li>
                    <li><strong>Legitimate Interest</strong>: Service improvement, security, and fraud prevention</li>
                    <li><strong>Contract Performance</strong>: Providing requested moodboard generation services</li>
                    <li><strong>Legal Obligation</strong>: Compliance with applicable laws and regulations</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Data Subject Rights (GDPR)</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Right of Access</strong>: Request information about personal data processing</li>
                    <li><strong>Right to Rectification</strong>: Correct inaccurate or incomplete data</li>
                    <li><strong>Right to Erasure</strong>: Request deletion of personal data ("right to be forgotten")</li>
                    <li><strong>Right to Restrict Processing</strong>: Limit how we process your data</li>
                    <li><strong>Right to Data Portability</strong>: Receive your data in a portable format</li>
                    <li><strong>Right to Object</strong>: Object to processing based on legitimate interests</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Contact Information</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Privacy Inquiries</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Email</strong>: panyietelka@yahoo.com</li>
                    <li><strong>Address</strong>: Budapest, Hamzsabegi ut 60</li>
                    <li><strong>Response Time</strong>: We will respond to privacy inquiries within 30 days</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Data Protection Officer</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Contact</strong>: panyietelka@yahoo.com</li>
                    <li><strong>Purpose</strong>: Handle complex privacy requests and compliance matters</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Legal Requests</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Law Enforcement</strong>: We will comply with valid legal requests for user data</li>
                    <li><strong>Court Orders</strong>: Data disclosure only with proper legal process</li>
                    <li><strong>User Notification</strong>: We will notify users of legal requests when legally permitted</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Dispute Resolution</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Complaint Process</h3>
                  <ol className="list-decimal list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Internal Resolution</strong>: Contact us first to resolve privacy concerns</li>
                    <li><strong>Regulatory Complaints</strong>: File complaints with relevant data protection authorities</li>
                    <li><strong>Arbitration</strong>: Binding arbitration for disputes (if applicable)</li>
                  </ol>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Applicable Law</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Governing Law</strong>: Curia of Hungary</li>
                    <li><strong>Jurisdiction</strong>: Courts of Curia of Hungary have exclusive jurisdiction</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Service-Specific Privacy Information</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">AI Processing Transparency</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Model Information</strong>: We use CLIP (Contrastive Language-Image Pre-training) for aesthetic classification</li>
                    <li><strong>Training Data</strong>: Our AI models are trained on publicly available datasets</li>
                    <li><strong>Bias Mitigation</strong>: We actively work to reduce bias in our aesthetic classifications</li>
                    <li><strong>Human Review</strong>: AI classifications may be reviewed by human experts for quality assurance</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Moodboard Generation Process</h3>
                  <ol className="list-decimal list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Image Analysis</strong>: Your uploaded image is analyzed for fashion aesthetics</li>
                    <li><strong>Keyword Generation</strong>: Relevant search terms are generated based on detected aesthetics</li>
                    <li><strong>Content Fetching</strong>: Third-party APIs are queried for complementary images</li>
                    <li><strong>Similarity Matching</strong>: AI ranks images by visual similarity to your original</li>
                    <li><strong>Moodboard Assembly</strong>: Final moodboard is created with proper attribution</li>
                  </ol>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Data Minimization</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li><strong>Collection Limitation</strong>: We only collect data necessary for service provision</li>
                    <li><strong>Purpose Limitation</strong>: Data is used only for stated purposes</li>
                    <li><strong>Retention Limitation</strong>: Data is retained only as long as necessary</li>
                    <li><strong>Accuracy</strong>: We maintain accurate and up-to-date information</li>
                  </ul>
                </div>
              </div>
            </section>

            <p className="text-gray-700 leading-relaxed text-lg mt-8">
              <strong>This Privacy Policy is effective as of January 1, 2025, and will remain in effect except with respect to any changes in its provisions in the future, which will be in effect immediately after being posted on this page.</strong>
            </p>

            <p className="text-gray-700 leading-relaxed text-lg mt-4">
              <strong>By using our service, you acknowledge that you have read and understood this Privacy Policy and agree to be bound by its terms.</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;

