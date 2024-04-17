
const activityJsonFilePath = document.getElementById("activityJsonFilePath").getAttribute("data-path");
fetch(activityJsonFilePath)
        .then(response => response.json())
        .then(data => {
            const activityNameDropdown = document.getElementById('activity-name');
            const activityDescriptionDropdown = document.getElementById('activity-description');
            const metValueInput = document.getElementById('met-value');


            const populateActivityNames = () => {
                const emptyOption = document.createElement('option');
                emptyOption.textContent = '';
                activityNameDropdown.appendChild(emptyOption);
                const uniqueActivityNames = [...new Set(data.map(item => item.ACTIVITY))];
                uniqueActivityNames.forEach(activityName => {
                    const option = document.createElement('option');
                    option.textContent = activityName;
                    activityNameDropdown.appendChild(option);
                });
            };


            const populateActivityDescriptions = (selectedActivityName) => {
                const emptyOption = document.createElement('option');
                emptyOption.textContent = '';
                activityDescriptionDropdown.appendChild(emptyOption);
                data.filter(item => item.ACTIVITY === selectedActivityName).forEach(item => {
                    const option = document.createElement('option');
                    option.textContent = item.SPECIFIC_MOTION;
                    activityDescriptionDropdown.appendChild(option);
                });
            };

            const fillMETValue = (selectedActivityDescription) => {
                const selectedActivity = data.find(item => item.SPECIFIC_MOTION === selectedActivityDescription);
                if (selectedActivity) {
                    metValueInput.value = selectedActivity.METs;
                }
            };


            activityNameDropdown.addEventListener('change', (event) => {
                const selectedActivityName = event.target.value;
                populateActivityDescriptions(selectedActivityName);

            });


            activityDescriptionDropdown.addEventListener('change', (event) => {
                const selectedActivityDescription = event.target.value;
                fillMETValue(selectedActivityDescription);
            });


            populateActivityNames();
        })
        .catch(error => console.error('Error fetching MET values:', error));