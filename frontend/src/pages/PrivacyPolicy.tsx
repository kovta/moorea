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
              <p className="text-gray-700 leading-relaxed text-lg">
                Our service integrates with third-party APIs to enhance your moodboard experience:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg mt-4">
                <li><strong>Unsplash API</strong>: For sourcing high-quality lifestyle and fashion imagery</li>
                <li><strong>Pexels API</strong>: Additional image curation and content discovery</li>
                <li><strong>Pinterest API</strong>: Fashion inspiration and trend analysis (with user consent)</li>
              </ul>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                These integrations help us provide diverse, relevant content for your moodboards while maintaining your privacy and data security.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Data Security</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                We implement industry-standard security measures to protect your personal information:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg mt-4">
                <li><strong>Encryption</strong>: All data transmission uses HTTPS/TLS encryption</li>
                <li><strong>Secure Storage</strong>: User credentials are hashed with SHA256 and salted</li>
                <li><strong>Access Controls</strong>: Strict access controls and regular security audits</li>
                <li><strong>Data Minimization</strong>: We only collect and retain data necessary for service provision</li>
              </ul>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Your Rights and Choices</h2>
              <div className="space-y-4">
                <p className="text-gray-700 leading-relaxed text-lg">
                  You have several rights regarding your personal information:
                </p>
                <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                  <li><strong>Access</strong>: Request a copy of your personal data</li>
                  <li><strong>Correction</strong>: Update or correct your information</li>
                  <li><strong>Deletion</strong>: Request deletion of your account and associated data</li>
                  <li><strong>Portability</strong>: Export your data in a structured format</li>
                  <li><strong>Opt-out</strong>: Withdraw consent for non-essential processing</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Contact Us</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                If you have any questions about this Privacy Policy or our data practices, please contact us at:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg mt-4">
                <p className="text-gray-800 font-medium">Email: privacy@moorea.app</p>
                <p className="text-gray-800 font-medium">Address: [Company Address]</p>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">Changes to This Policy</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the "Last Updated" date.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
              <p className="text-gray-700 leading-relaxed mb-4">
                We use industry-standard security measures to protect your data. Your images and personal information 
                are stored securely using encrypted databases and secure cloud storage. We do not share your personal 
                information with third parties except as necessary to provide our service.
              </p>
              
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Pinterest Data - No Storage Policy</h3>
                <p className="text-gray-700 leading-relaxed mb-2">
                  <strong>We do NOT store any Pinterest data.</strong> In compliance with Pinterest's Developer Guidelines, 
                  we follow a strict "no storage" policy:
                </p>
                <ul className="list-disc list-inside text-gray-700 ml-4 space-y-1">
                  <li>We call Pinterest API each time we need content - never from cache or stored data</li>
                  <li>Pinterest data exists only temporarily in-memory during moodboard generation</li>
                  <li>No Pinterest URLs, metadata, or content is stored in our database</li>
                  <li>No Pinterest data is cached, even temporarily</li>
                  <li>Pinterest images are excluded from saved moodboards</li>
                  <li>All Pinterest data is discarded immediately after use</li>
                </ul>
                <p className="text-gray-700 leading-relaxed mt-2 text-sm">
                  Pinterest content is used only for immediate display and linking back to original pins for attribution. 
                  We never store, cache, or persist any information from Pinterest API.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Your Rights</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                You have the right to:
              </p>
              <ul className="list-disc list-inside text-gray-700 ml-4 space-y-1">
                <li>Access your personal data</li>
                <li>Request correction of inaccurate data</li>
                <li>Request deletion of your data</li>
                <li>Opt out of marketing communications</li>
                <li>Withdraw consent at any time</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Contact Us</h2>
              <p className="text-gray-700 leading-relaxed">
                If you have questions about this privacy policy or wish to exercise your rights, please contact us at:
              </p>
              <p className="text-gray-700 mt-2">
                <a 
                  href="mailto:annaszilviakennedy@gmail.com" 
                  className="text-purple-600 hover:text-purple-800 underline"
                >
                  annaszilviakennedy@gmail.com
                </a>
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Changes to This Policy</h2>
              <p className="text-gray-700 leading-relaxed">
                We may update this privacy policy from time to time. We will notify you of any changes by posting 
                the new policy on this page and updating the "Last updated" date.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;

