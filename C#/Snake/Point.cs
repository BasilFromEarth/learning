using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snake_OOP___learn_
{
    class Point
    {
        public int x, y;
        public char sym;




        public Point(int x_, int y_, char sym_)
        {
            x = x_;
            y = y_;
            sym = sym_;
        }

        public Point(Point tail)
        {
            x = tail.x;
            y = tail.y;
            sym = tail.sym;
        }


        public void Draw()
        {
            Console.SetCursorPosition(x,y);
            Console.Write(sym);
        }

        public void Clear()
        {
            sym = ' ';
            Draw();
        }

        public void Move(int i, Direction d)
        {

            switch (d)
            {
                case Direction.RIGHT:
                    x += i;
                    break;

                case Direction.LEFT:
                    x -= i;
                    break;

                case Direction.UP:
                    y -= i;
                    break;

                case Direction.DOWN:
                    y += i;
                    break;
            }

        }
    }
}
