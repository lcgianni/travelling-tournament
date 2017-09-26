import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;


public class TSP {
	public static void main(String[] args) throws IOException {

		//Prepare for user input
		BufferedReader userinput = new BufferedReader(new
				InputStreamReader(System.in));

		//Get file name
		String fileName = "";
		System.out.println("Place dataset in root folder and type filename (ex: data8.txt):");
		fileName = userinput.readLine();


		//Start counter
		long startTime = System.currentTimeMillis();

		//Read in each distance from the distance matrix within the text file
		Scanner readFile;
		readFile = new Scanner(new File(fileName));

		//find size of problem based on input file
		int n = 0; 
		do{
			readFile.nextInt();
			n++;
		}while(readFile.hasNext());
		n = (int) Math.sqrt(n);//take square root of total number of integers in file to get number of cities
		readFile.close();//exhausted hasNext(), close file



		//Create distance matrix
		int[][] cityDistances = new int[n][n];
		int i = 0;
		int j = 0;

		readFile = new Scanner(new File(fileName));

		//Populate distance matrix
		for(j=0;j<n;j++){
			for(i=0;i<n;i++){
				cityDistances [i][j] = readFile.nextInt();
			}
		}
		readFile.close();//close file


		int ha = 0;
		//Max consecutive home and away games
		while(ha > n-1 || ha <= 0){ 

			System.out.println("Input consecutive maximum home/away games: ");
			ha = Integer.parseInt(userinput.readLine());

			if(ha > n-1 || ha <= 0){
				System.out.println("Invalid value entered. Value must be greater than 0 and less than (# of Teams - 1): ");
			}
		}



		int [][]starWeight = new int [n][1];
		int indexWeight = 0;


		//Obtain star weights for each city
		for(j=0;j<n;j++){
			for(i=0;i<n;i++){
				starWeight[j][0] += cityDistances[i][j];
			}
		}

		//Initialize star weight
		int tempWeight = 10000000;

		//Identify minimum star weight
		for(i=0;i<n;i++){
			if(starWeight[i][0]<tempWeight){	
				tempWeight = starWeight[i][0];
				indexWeight = i;
			}
		}
		
		System.out.println(starWeight[indexWeight][0]+" is the minimum star weight which belongs to index " + indexWeight);
		System.out.println();

		//TSP Solver
		int[]chosenPath = new int [n+1];
		int distance = 0;
		
		//Populate initial path
		for(i=1;i<n;i++){
			if(i!=indexWeight){
				chosenPath[i] = i;
			}
		}
		
		//Set minimum star weight as beginning/end node
		chosenPath [0] = indexWeight;
		chosenPath [n] = indexWeight; 

		//calculate total distance
		for(i=0;i<n;i++){
			distance += cityDistances[chosenPath[i]][chosenPath[i+1]];
		}
		
		int tempDistance=0;
		int [] tempPath = new int[n+1];
		int tempHold = 0;
		
		//Copy starting path
		for(i=0;i<n+1;i++){ 
			tempPath[i] = chosenPath[i];
		}
		
		//start swaps
		int count = 0;

		//Begin first accept algorithm
		while(count!=100){
			
			for(j=1;j<n-1;j++){
				for(i=1;i<n-1;i++){
					//Begin swapping nodes, but leave minimum star weight node alone
					tempHold=tempPath[j];
					tempPath[j]=tempPath[i];
					tempPath[i]=tempHold;
					tempDistance = 0;
					
					//Calculate distance of new proposed path
					for(int z=0;z<n;z++){
						tempDistance += cityDistances[tempPath[z]][tempPath[z+1]];
					}
					//Check if the proposed path is better, and if so replace
					if(tempDistance<distance){
						for(int b=0;b<n+1;b++){
							chosenPath[b]=tempPath[b];

						}
						distance = tempDistance;	
						
						System.out.println("Shortest TSP path found so far: " + distance);//as better paths are found...

					}
					
					//revert change to tempPath
					else{
						tempHold=tempPath[i];
						tempPath[i]=tempPath[j];
						tempPath[j]=tempHold;

					}

				}

			}
			//For the while loop
			count++;
		}



		System.out.println();
		System.out.println("Best TSP path found so far with star weight constraint: " );
		
		//Print best path found
		for(int a=0;a<n+1;a++){
			if(a!=n){
				System.out.print(chosenPath[a]+ "->");
			}
			else {
				System.out.print(chosenPath[a]);
			}}
		System.out.println();
		System.out.println("With a distance of: " + distance);
		



		//The next algorithm requires a specific format of the TSP solution
		int pathFormatted[] = new int [n];
		
		//Only the last node is the minimum star weight
		for(i=0;i<pathFormatted.length;i++){
			pathFormatted[i]=chosenPath[i+1];
		}
		
		System.out.println();
		System.out.println("Reformatting path for use in part 2... ");
		System.out.println();
		//Print out the reformatted path
		for(int a=0;a<n;a++){
			if(a!=(n-1))
				System.out.print(pathFormatted[a]+ "->");
			else System.out.print(pathFormatted[a]);
		}
		System.out.println();
		System.out.println();
		
		//Create TTP schedule matrix
		int [][]schedule = new int [n][2*n-2];
		
		//Pass onto the next algorithm
		schedule = part2.part2(ha,pathFormatted,n); 

		//Get distances
		int []teamDistance= new int [n];
		int totalDistance = 0;

		for(j=0;j<n;j++){
			for(i=0;i<(2*n-3);i++){

				if(i==0 && schedule[j][i]<0){
					//First game away
					//Note: (schedule[j][i])-1) due to the city numbers being increased by +1 to avoid the issue with -0 = 0
					teamDistance[j] += cityDistances[j][Math.abs(schedule[j][i])-1];
				}
				
				//2x home games or (1home 1away)
				if(schedule[j][i]>0){
					
					//not going anywhere 2x home
					if(schedule[j][i+1]>0){
						teamDistance[j] += cityDistances[j][j]; 
					}
					//1 home, 1 away
					else{
						teamDistance[j] += cityDistances[j][Math.abs(schedule[j][i+1])-1];
					}

				}
				//1away 1home
				else if(schedule[j][i+1]>0){
					teamDistance[j] += cityDistances[Math.abs(schedule[j][i])-1][j];
				}

				//2 away
				else{teamDistance[j] += cityDistances[Math.abs(schedule[j][i])-1][Math.abs(schedule[j][i+1])-1];
				}
				
				//If last game away return home
				if(i==(2*n-4) && schedule [j][i+1]<0){
					teamDistance[j] += cityDistances[j][Math.abs(schedule[j][i+1])-1];
				}
			}
			
			
			
			
			//Print out each team's travel distance
			System.out.println("Team "+(j+1)+ " has a total travel distance of: " + teamDistance[j]);
			totalDistance += teamDistance[j];
		}
		//Total distance traveled by all teams
		System.out.println();
		System.out.println("Total Team Travel Distance: " + totalDistance);
		System.out.println();
		//Total computation time
		long endTime = System.currentTimeMillis();
		System.out.println("Total time: " + (endTime-startTime) + "ms");

		//Write schedule to file
		BufferedWriter out= new BufferedWriter(new FileWriter("Solution "+fileName)); 
		for (int a=0; a<n;a++){
			for(int b=0;b<2*n-2;b++){
				out.write(String.valueOf(schedule[a][b]));
				out.write("\t");
			}
			out.newLine();
		}
		out.close();

	}


}




