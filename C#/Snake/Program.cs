using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace snake_OOP___learn_
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.SetWindowSize(80,26);
            Console.SetBufferSize(81, 26);

            Walls walls = new Walls(80, 26);
            walls.Draw();

            Point p = new Point(10, 5, '*');

            Snake snake = new Snake(p, 3, Direction.RIGHT);
            snake.Draw();

            Food f = new Food(80, 25, '$');
            Point food = f.CreateFood();
            food.Draw();

            while (true)
            {
                if(snake.IsHitTail() || walls.isHit(snake))
                {
                    break;
                }


                if (snake.Eat(food))
                {
                    food = f.CreateFood();
                    food.Draw();
                    snake.pList.Insert(0, snake.pList.First());
                }
                

                if (Console.KeyAvailable)
                {
                    ConsoleKeyInfo key = Console.ReadKey();
                    snake.HandleKey(key);
                }
               
                    Thread.Sleep(100);
                    snake.Move();
                
            }

            Console.ReadLine();
        }
    }
}
