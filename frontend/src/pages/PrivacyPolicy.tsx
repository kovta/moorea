import React from 'react';
import { Link } from 'react-router-dom';

const PrivacyPolicy: React.FC = () => {
  return (
    <div className="min-h-screen gradient-bg p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <div className="mb-8">
            <Link 
              to="/" 
              className="text-purple-600 hover:text-purple-800 inline-flex items-center gap-2 mb-6"
            >
              <span>←</span>
              Back to Home
            </Link>
            <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">
              Privacy Policy
            </h1>
            <p className="text-gray-600 text-sm">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>

          <div className="prose prose-gray max-w-none space-y-6">
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Introduction</h2>
              <p className="text-gray-700 leading-relaxed">
                Welcome to Moorea. We respect your privacy and are committed to protecting your personal data. 
                This privacy policy explains how we collect, use, and safeguard your information when you use our service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Information We Collect</h2>
              <div className="space-y-3">
                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">Personal Information</h3>
                  <p className="text-gray-700 leading-relaxed">
                    When you sign up for our waitlist or create an account, we collect:
                  </p>
                  <ul className="list-disc list-inside text-gray-700 ml-4 space-y-1">
                    <li>Email address</li>
                    <li>Name (optional)</li>
                    <li>Account credentials (if you create an account)</li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">Usage Data</h3>
                  <p className="text-gray-700 leading-relaxed">
                    We automatically collect information about how you use our service, including:
                  </p>
                  <ul className="list-disc list-inside text-gray-700 ml-4 space-y-1">
                    <li>Images you upload for moodboard generation</li>
                    <li>Moodboards you create and save</li>
                    <li>Preferences and aesthetic selections</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">How We Use Your Information</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                We use the information we collect to:
              </p>
              <ul className="list-disc list-inside text-gray-700 ml-4 space-y-1">
                <li>Provide and improve our moodboard generation service</li>
                <li>Process your waitlist signup and notify you when we launch</li>
                <li>Personalize your experience and generate relevant moodboards</li>
                <li>Communicate with you about our service</li>
                <li>Ensure the security and functionality of our platform</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-3">Data Storage and Security</h2>
              <p className="text-gray-700 leading-relaxed">
                We use industry-standard security measures to protect your data. Your images and personal information 
                are stored securely using encrypted databases and secure cloud storage. We do not share your personal 
                information with third parties except as necessary to provide our service.
              </p>
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

