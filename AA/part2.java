import java.io.IOException;

public class part2 {
public static int[][] part2(int ha, int[] teams, int n) throws IOException
{
	
//nodes = the team that is on that node of the graph where nodes(1) is
//always team n which has the smallest star length
int[] nodes = new int[n];
nodes[0]= teams[n-1];

//Matching order of nodes with teams
int a; int b=2;
for (a=1; a<n; a++)
{
	if (a<=n/2)
		nodes[2*a-1]=teams[a-1];
	else
	{
		nodes[b]=teams[a-1];
		b=b+2;
	}
}

//Setting up a home-away vector (+1 or -1 values)
int[] havector = new int [n];
int number=-1; //number=-1 -> away; number=1 -> home

//first half of home-away vector (first round)
for (a=0;a<((int)n/ha/2)*ha; a=a+ha) //CHANGED FROM n/ha  to int n/ha/2 * ha
{
		for(b=0;b<ha;b++)
			havector[a+b]=number; 	
		number=number*-1;
}

double i = (Math.floor(n/(2*ha)))*ha;
for(a=(int)i; a<n/2;a++)
	havector[a]=number; 

//second half = negative mirror of first half (first round)
for(a=0;a<n/2;a++)
	havector[a+n/2]=-1*havector[n/2-a-1]; 

//setting up array for schedule
int[][] schedule = new int [n][2*n-2];
int r; int k;

//rounds in first half of tournaments
for(r=0; r<n-1;r++)
{
	//for rounds>1, switch the home/away value on first node (if there has been 
	//a max # of home/away games in a row
	
	if(r!=0 && r%ha==0)
	{
		havector[0]=-1*havector[0];
		havector[n-1]=-1*havector[n-1];
	}
	
	//schedule for round r
	k=n-1;
	for(a=0;a<n;a++)
	{
		schedule[nodes[a]][r] = havector[a]*(1+nodes[k]); 
		k=k-1;
	}
	
	//Move all but the first node counter-clockwise one position
	int temp = nodes[1];
	for (a=1; a<n-1; a++)
		nodes[a]=nodes[a+1];
	nodes[n-1]=temp;
}

//second half of tournament (opposite of round n-2, n-1, 1, 2, ..., n-3)
a=n-2;
for(r=n-1;r<2*n-2;r++)
{
	for(b=0;b<n;b++) //b=team 
		schedule[b][r]=-1*schedule[b][a-1];
	a=a+1;
	if (a==n)
		a=1;	
}


//printing/displaying resulting schedule
System.out.println("Team Schedule:");
for (a=0; a<n;a++){
	for(b=0;b<2*n-2;b++){
		System.out.print(schedule[a][b]);
		System.out.print("\t");
	}
	System.out.print("\n");
}
System.out.println();
return schedule; 

}
}


