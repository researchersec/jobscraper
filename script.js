document.addEventListener('DOMContentLoaded', function() {
    fetch('it/data.json')
        .then(response => response.json())
        .then(data => {
            const jobListings = document.getElementById('job-listings');
            data.forEach(job => {
                const jobCard = document.createElement('div');
                jobCard.className = 'job-card';
                jobCard.innerHTML = `
                    <h2>${job.title}</h2>
                    <p><strong>Company:</strong> ${job.company}</p>
                    <p><strong>Location:</strong> ${job.location}</p>
                    <p><strong>Date:</strong> ${job.pub_date}</p>
                    <a href="${job.job_URL}" target="_blank">View Job</a>
                `;
                jobListings.appendChild(jobCard);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
