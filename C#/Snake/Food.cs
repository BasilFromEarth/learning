using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snake_OOP___learn_
{
    class Food
    {
        int mapHeight;
        int mapWidth;
        char sym;

        Random random = new Random();

        public Food(int mapWidth, int mapHeight, char sym)
        {
            this.mapHeight = mapHeight;
            this.mapWidth = mapWidth;
            this.sym = sym;
        }

        public Point CreateFood()
        {
            int w = random.Next(2, mapWidth - 2);
            int h = random.Next(2, mapHeight - 2);

            return new Point(w, h, sym);
        }
    }
}
