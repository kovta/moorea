import React from 'react';
import { Link } from 'react-router-dom';

const Terms: React.FC = () => {
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
