
const foodJsonFilePath = document.getElementById("foodJsonFilePath").getAttribute("data-path");

fetch(foodJsonFilePath)
        .then(response => response.json())
        .then(data => {
            const foodInput = document.getElementById('foodInput');
            const foodGroup = document.getElementById('foodGroup');
            const calorie = document.getElementById('calorieInput');
            console.log(foodGroup)
            const searchResults = document.getElementById('searchResults');

            const filterOptions = () => {
                const searchText = foodInput.value.toLowerCase();
                searchResults.innerHTML = '';

                const filteredData = data.filter(item => item.name.toLowerCase().includes(searchText));

                for (let i = 0; i < Math.min(filteredData.length, 20); i++) {
                    const result = filteredData[i];
                    const option = document.createElement('a');
                    option.textContent = result.name;
                    option.addEventListener('click', () => {
                        foodInput.value = result.name;
                        foodGroup.value = result.foodGroup;
                        calorie.value = result.Calories;
                        console.log(calorie.value)
                        searchResults.classList.remove('show');
                    });
                    searchResults.appendChild(option);
                }

                if (searchText.length > 0 && filteredData.length > 0) {
                    searchResults.classList.add('show');
                } else {
                    searchResults.classList.remove('show');
                }
            };

            foodInput.addEventListener('input', filterOptions);
        })
        .catch(error => console.error('Error fetching JSON:', error));