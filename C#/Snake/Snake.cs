using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snake_OOP___learn_
{
    enum Direction              //Перелік для зрозумілого задання напрямку руху
    {
        LEFT,RIGHT,UP,DOWN
    }

    class Snake : Figure         //Клас, реалізуючий нашу змійку
    {
        Direction direction;

        public Snake(Point tail, int length, Direction direction_) //Передаємо в конструктор координату хвоста, довжину, напрям
        {
            pList = new List<Point>();

            direction = direction_;

            for(int i = 0; i < length; i++)    //Заповнюємо колецію, в якій і буде зберігатися змійка                                                                                                                                                                    ь                                                                                                                                                                                                                                                                                                                                                                               
            {
                Point p = new Point(tail);     
                p.Move(i, direction);
                pList.Add(p);
            }

        }

        internal void Move()
        {
            Point tail = pList.First();
            pList.Remove(tail);

            Point head = GetNextPoint();
            pList.Add(head);

            tail.Clear();
            head.Draw();
        }

        public Point GetNextPoint()
        {
            Point head = pList.Last();
            Point nextPoint = new Point(head);

            nextPoint.Move(1, direction);

            return nextPoint;
        }

        public void HandleKey(ConsoleKeyInfo key)
        {
            switch (key.Key)
            {
                case ConsoleKey.UpArrow:
                    direction = Direction.UP;
                    break;
                case ConsoleKey.DownArrow:
                    direction = Direction.DOWN;
                    break;
                case ConsoleKey.LeftArrow:
                    direction = Direction.LEFT;
                    break;
                case ConsoleKey.RightArrow:
                    direction = Direction.RIGHT;
                    break;
            }
        }

        public bool Eat(Point food)
        {
            Point head = pList.Last();
            if (food.x == head.x && food.y == head.y)
                return true;
            else
                return false;
        }

        public bool IsHitTail()
        {
            var head = pList.Last();

            for(int i = 0; i < pList.Count - 2; i++)
            {
                var pp = pList[i];

                if (head.x == pp.x && head.y == pp.y)
                    return true;
            }

            return false;
        }

    }
}
