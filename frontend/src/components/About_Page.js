import React from 'react';

const AboutPage = ({ onNavigate }) => (
  <div className='page-container'>
    <div className="page-header">
      <h1>About</h1>
      <button className="back-button" onClick={() => onNavigate('dashboard')}>
        Back to Dashboard
      </button>
    </div>
    <div className="page-content">
      <h2>About This Website</h2>
      <p>
      This is a surf reporting application that gives real-time data based on:
      <br />
      • Live buoy data from real buoys in respective locations
      <br />
      • Computer vision and machine learning model that detects surfers in live surf cameras
      </p>
      <div className="settings-section">
        <h3>How the Real-Time Surfer Detection Works</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">Live Surf Camera to Surf Reporter Pipeline</div>
            <p className="setting-description">
              The complete data pipeline begins with the live surf camera stream via HLS. HLS is ingested by FFmpeg and serves the converted MJPEG stream via a local HTTP endpoint. MJPEG stream becomes the input source for inference, with each camera running in a respective thread for parallel processing. Robotflow's InferencePipeline is initialized, pulling frames from the MJPEG stream. Frame-by-frame inference occurs when sent to Roboflow’s hosted object detection model. Surfer count is recorded and counted from the predictions and updated to a global dictionary. Flask serves a route that reads from the global dictionary and returns the response in JSON format. The frontend fetches and queries this in a specified time interval. The response data is passed into the React state and displayed. Users see a real-time surfer count on the main page. 
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Computer Vision & Machine Learning Elements</div>
            <p className="setting-description">
              This application leverages Roboflow as the foundation for computer vision and machine learning functionality, focused on detecting surfers in real-time from surf camera footage. I. Ryan Fabrick, built a custom-trained object detection model using Roboflow's 3.0 Object Detection (Fast) framework. It is designed to detect surfers within video frames, outputting bounding boxes around detected surfers, confidence scores, and class labels.
              <br /><br />
              The model yields a mean average precision at 0.5 lou (mAP@50) of 65.4%, which measures the overlap between predicted and ground-truth boxes. It yields a precision of 69.3%, meaning 6.93 out of 10 predictions are correct. It yields a recall of 63.9%, indicating it successfully detects nearly two-thirds of all actual surfers in a frame.
              <br /><br />
              For real-time deployment, this application uses Roboflow's InferencePipeline class to connect the model to live MJPEG video streams. This pipeline handles video frame extraction and automatically invokes the object detection model at a specified frame rate. A custom callback function is used to parse predictions returned as structured data. This counts the number of surfers per frame and pushes the result to be accessible to the rest of the application.
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Stream Processing</div>
            <p className="setting-description">
              The stream processing component of this application converts raw, public surf camera feeds into a format suitable for frame-by-frame analysis by the machine learning model. Surf cams are used to provide video streams via HTTP Live Streaming (HLS), which provides video in segmented .m3u8 playlist files. Each .m3u8 file lists a sequence of short MPEG video chunks that update in near real-time. 
              <br /><br />
              This application uses FFmpeg, a multimedia tool, to convert HLS streams into Motion JPEG (MJPEG) format. To achieve this, a subprocess is launched that reads the HLS stream and transcodes it into a new stream served over HTTP locally. Conditions such as frame rates and resolution standardization are passed during this. The output stream is hosted via a local server on a unique port, which serves a continuous MJPEG feed suitable for CV ingestion. 
              <br /><br />
              Each surf camera used is processed in a dedicated thread, allowing the system to handle multiple streams concurrently. Each thread monitors the health of its respective FFMpeg process and can restart if the process fails. MJPEF streams simplify downstream processing which makes it easier to extract, analyze, and discard frames in real-time. This enables fast and reliable frame delivery to the Roboflow inference engine. 
            </p>
          </div>
        </div>
        <div className="setting-item" id="CV-annotated-example">
          <div>
            <div className="setting-label">Computer Vision & Machine Learning Model in Action</div>
            <p className="setting-description">
              <video width="100%" controls>
                <source src="/videos/Example_Video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section" id="data-metrics-section">
        <h3>Data Metric Meanings</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">Wave Height (Hs)</div>
            <p className="setting-description">
              Signficant wave height is defined as the average height (meters) of the highest 
              one-third of waves. 
              <strong> This gives a good estimate of how big the waves will feel in the lineup for surfers!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak Period (Tp)</div>
            <p className="setting-description">
              The peak period is defined as the time interval (seconds) between waves with
              with the highest energy. This indicates the frequency of the dominant wave system. 
              <strong> Longer peak periods typically mean more powerful, cleaner, and better-shaped waves for surfing!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Wave Direction (Dp)</div>
            <p className="setting-description">
              Wave direction is defined as as the directions (degrees tru) from which the peak
              energy waves are coming. 
              <strong> This helps surfers determine whether a particular break will be working based on how swell hits the coastline!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Average Period (Ta)</div>
            <p className="setting-description">
              The average period is defined as a representation of the mean time between all waves in the
              specturm, weighted by energy. It reflects the general energy distribution across all
              wave frequencies. 
              <strong> It gives surfers a sense of overall swell consistency and helps distinguish between mixed swell energy!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Zero Up-Crossing Period (Tz)</div>
            <p className="setting-description">
              Zero up-crossing period is defiend as the average time between upward crossings of the mean sea 
              level by wave crests. 
              <strong> Surfers can use this to gauge wave rhythm and timing. Shorter periods usually mean choppier conditions!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak PSD</div>
            <p className="setting-description">
              Peak power spectral density is defined as the highest energy value (m²/Hz) found in the wave spectrum. 
              <strong> Higher PSD means more focused swell energy, often translating into stronger and more surfable waves!</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>Data Sources & Credits</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">Buoys</div>
            <p className="setting-description">
              <a href="https://cdip.ucsd.edu/" target="_blank" rel="noopener noreferrer" style={{color: '#E0B0FF'}}>Coastal Data Information Program (CDIP)</a>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Surf Cameras</div>
            <p className="setting-description">
              <a href="https://thesurfersview.com/" target="_blank" rel="noopener noreferrer" style={{color: '#E0B0FF'}}>The Surfers View</a>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Other</div>
            <p className="setting-description">
              <a href="https://roboflow.com/" target="_blank" rel="noopener noreferrer" style={{color: '#E0B0FF'}}>Roboflow</a>
              <br />
              <a href="https://ffmpeg.org/" target="_blank" rel="noopener noreferrer" style={{color: '#E0B0FF'}}>FFmpeg</a>
            </p>
          </div>
        </div>
      </div>

      
      <div className="settings-section">
        <h3>Public GitHub Repository</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">GitHub Repository Link</div>
            <p className="setting-description">
              repo link here
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

);

export default AboutPage;