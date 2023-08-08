// LessonVisualization.js

import React from 'react';

const LessonVisualization = ({ jsonData }) => {
  return (
    <div className="lesson-visualization">
      {jsonData.map((lessonData) => (
        <div key={lessonData.LessonNumber} className="lesson-box">
          <h3>Lesson {lessonData.LessonNumber}</h3>
          <div className="activities-box">
            {lessonData.Activities.map((activity, index) => (
              <div key={index} className="activity-capsule">
                <span className="activity-name">{activity[0]}</span>
                <span
                  className="activity-score"
                  style={{ color: activity[1] >= 4 ? 'Chartreuse' : 'inherit' }}
                >
                  ({activity[1]})
                </span>
                <span className="activity-status" style={{ color: 'green' }}>
                  {activity[2] === 'Graded' ? '✔' : activity[2] === 'Skipped' ? '(Skipped) ' : ''}
                </span>
                <span className="activity-notes">{activity[3]}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default LessonVisualization;
