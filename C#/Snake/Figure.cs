using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snake_OOP___learn_
{
    class Figure //Батьківський клас
    {
        public List<Point> pList = new List<Point>(); //Декларуємо колекцію

        public void Draw()  //Виводимо наш екземпляр 
        {
            foreach (Point p in pList)
                p.Draw();
        }

        public bool IsHit(Figure figure)
        {
            foreach (var p in pList)
            {
                if (figure.IsHit(p))
                    return true;
            }

            return false;
        }

        private bool IsHit(Point point)
        {
            foreach (var p in pList)
            {
                if (point.x == p.x && point.y == p.y)
                    return true;
            }
            return false;
        }
    }
}
