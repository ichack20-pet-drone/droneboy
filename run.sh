cd pet-drone
npm install

# Run server
cd server
npm install
node src/app.js &

# Run vue
cd ..
npm run serve &

# Run drone boy
cd ../src
python3 drone_boy.py
