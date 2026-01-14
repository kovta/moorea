import React from 'react';
import { Link } from 'react-router-dom';

const Terms: React.FC = () => {
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
              Terms of Service
            </h1>
            <p className="text-gray-600 text-sm mb-8">
              Effective Date: January 1, 2025 | Last Updated: January 9, 2026
            </p>
          </div>

          <div className="prose prose-lg prose-gray max-w-none space-y-8">
            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                By accessing and using the Moodboard Generator service ("Service," "App," or "Platform"), you agree to be bound by these Terms of Service ("Terms"). If you do not agree to these Terms, please do not use our Service.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                We reserve the right to modify these Terms at any time. Your continued use of the Service after changes become effective constitutes your acceptance of the updated Terms. We will notify you of material changes via email or prominent notice on the Service.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">2. Description of Service</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                Moodboard Generator is an AI-powered web application that:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg mt-4">
                <li>Accepts user-uploaded clothing or fashion item images</li>
                <li>Uses artificial intelligence (CLIP model) to identify fashion aesthetics and styles</li>
                <li>Generates personalized moodboards by curating lifestyle imagery and complementary fashion content from third-party APIs (Unsplash, Pexels, and potentially Pinterest)</li>
                <li>Allows users to save, organize, and share their generated moodboards</li>
                <li>Provides browsing and recommendation features based on identified aesthetics</li>
              </ul>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                The Service is provided "as-is" for personal, non-commercial use only.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">3. User Eligibility and Registration</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Age Requirements</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li>You must be at least 13 years of age to use this Service</li>
                    <li>If you are under 18, you represent that you have parental or guardian consent</li>
                    <li>Users under 13 are not permitted to create accounts or upload content</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Account Creation</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li>Account creation is optional for anonymous moodboard generation</li>
                    <li>Creating an account allows you to save, organize, and access your moodboard history</li>
                    <li>You agree to provide accurate, complete, and current information during registration</li>
                    <li>You are responsible for maintaining the confidentiality of your account credentials</li>
                    <li>You agree to notify us immediately of any unauthorized use of your account</li>
                    <li>You are responsible for all activities that occur under your account</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Account Termination</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li>You may delete your account at any time through your account settings</li>
                    <li>Upon account deletion, all associated data will be permanently removed within 30 days</li>
                    <li>We reserve the right to suspend or terminate accounts that violate these Terms</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">4. User-Generated Content and Uploaded Images</h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Image Upload and Processing</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li>By uploading an image to the Service, you grant us a non-exclusive, royalty-free license to process, analyze, and display that image for moodboard generation purposes</li>
                    <li>Uploaded images are processed using our AI classification system and are not permanently stored on our servers</li>
                    <li>Images are processed in-memory only and are deleted immediately after moodboard generation, unless you choose to save the moodboard to your account</li>
                    <li>If you save a moodboard, the associated uploaded image and metadata are retained until account deletion or 2 years of account inactivity</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-3">Content Ownership</h3>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                    <li>You retain ownership of all content you upload to the Service</li>
                    <li>You represent and warrant that you have the necessary rights to upload and use the content</li>
                    <li>You agree not to upload content that infringes on third-party rights or violates applicable laws</li>
                  </ul>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">5. Intellectual Property</h2>
              <div className="space-y-4">
                <p className="text-gray-700 leading-relaxed text-lg">
                  The Service and its original content, features, and functionality are owned by us and are protected by copyright, trademark, and other intellectual property laws.
                </p>
                <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg">
                  <li><strong>Service Content</strong>: All AI-generated moodboards, curated content, and service features are our intellectual property</li>
                  <li><strong>Third-Party Content</strong>: Images from Unsplash, Pexels, and Pinterest are subject to their respective licenses</li>
                  <li><strong>User License</strong>: You are granted a limited, non-exclusive license to use the Service for personal, non-commercial purposes</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">6. Prohibited Uses</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                You agree not to use the Service for any unlawful or prohibited purpose, including but not limited to:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-6 text-lg mt-4">
                <li>Uploading inappropriate, offensive, or illegal content</li>
                <li>Attempting to reverse engineer or copy our AI models</li>
                <li>Using automated tools to access the Service</li>
                <li>Impersonating other users or entities</li>
                <li>Distributing malware or harmful code</li>
                <li>Violating any applicable laws or regulations</li>
              </ul>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">7. Disclaimer of Warranties</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                The Service is provided on an "as-is" and "as-available" basis. We make no representations or warranties of any kind, express or implied, regarding the operation of the Service or the information, content, or materials included therein.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                We do not warrant that the Service will be uninterrupted, error-free, or secure, or that any defects will be corrected.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">8. Limitation of Liability</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                In no event shall we be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or related to your use of the Service, even if we have been advised of the possibility of such damages.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                Our total liability to you for any claims arising from your use of the Service shall not exceed the amount you paid us in the 12 months preceding the claim.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">9. Indemnification</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                You agree to indemnify and hold us harmless from any claims, damages, losses, or expenses arising from your use of the Service, your violation of these Terms, or your infringement of any rights of another party.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">10. Termination</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                We may terminate or suspend your account and access to the Service immediately, without prior notice, for any reason, including breach of these Terms.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                Upon termination, your right to use the Service will cease immediately, and we may delete your account and associated data.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">11. Governing Law</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                These Terms shall be governed by and construed in accordance with the laws of [Jurisdiction], without regard to its conflict of law provisions.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">12. Changes to Terms</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                We reserve the right to modify these Terms at any time. We will notify you of changes by posting the updated Terms on this page and updating the effective date.
              </p>
              <p className="text-gray-700 leading-relaxed text-lg mt-4">
                Your continued use of the Service after changes become effective constitutes acceptance of the updated Terms.
              </p>
            </section>

            <section>
              <h2 className="text-3xl font-semibold text-gray-900 mb-4">13. Contact Information</h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                If you have any questions about these Terms, please contact us at:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg mt-4">
                <p className="text-gray-800 font-medium">Email: legal@moorea.app</p>
                <p className="text-gray-800 font-medium">Address: [Company Address]</p>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Terms; 
              to="/" 
              className="text-purple-600 hover:text-purple-800 inline-flex items-center gap-2 mb-6"
            >
              <span>←</span>
              Back to Home
            </Link>
            <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">
              Terms of Service
            </h1>
            <p className="text-gray-600 text-sm">Last updated: {new Date().toLocaleDateString()}</p>
          </div>

          <div className="prose prose-gray max-w-none space-y-6">
            <section>
              <h2>Acceptance of Terms</h2>
              <p>
                By accessing and using Moorea ("Service"), you agree to be bound by these
                Terms of Service. If you do not agree, please do not use the Service.
              </p>
            </section>

            <section>
              <h2>Description of Service</h2>
              <p>
                Moorea provides AI-powered moodboard generation from uploaded clothing images using
                image classification and third-party content APIs (Unsplash, Pexels, etc.). The
                service is provided "as-is" for personal, non-commercial use.
              </p>
            </section>

            <section>
              <h2>User Content & Uploaded Images</h2>
              <p>
                By uploading images you grant Moorea a license to process and display the image
                for moodboard generation. You are responsible for ensuring you have rights to any
                images you upload and must not upload illegal, infringing, or explicit content.
              </p>
            </section>

            <section>
              <h2>Intellectual Property</h2>
              <p>
                Moorea and its contents are protected by intellectual property laws. Third-party
                images are subject to their providers' licenses and must be attributed when required.
              </p>
            </section>

            <section>
              <h2>Liability & Disclaimers</h2>
              <p>
                The Service is provided without warranties. To the maximum extent permitted by law,
                Moorea's liability is limited.
              </p>
            </section>

            <section>
              <h2>Governing Law</h2>
              <p>
                These Terms are governed by the laws of the State of California, U.S.A. Users
                agree to submit to the jurisdiction of courts located in California.
              </p>
            </section>

            <section>
              <h2>Contact</h2>
              <p>
                Questions? Contact us at{' '}
                <a href="mailto:annaszilviakennedy@gmail.com" className="text-purple-600 underline">annaszilviakennedy@gmail.com</a>.
              </p>
            </section>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Terms;
