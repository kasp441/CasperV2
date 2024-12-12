using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WebApplication1.Migrations
{
    /// <inheritdoc />
    public partial class lessComplications : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Category",
                table: "Reminders");

            migrationBuilder.DropColumn(
                name: "CreatedDate",
                table: "Reminders");

            migrationBuilder.DropColumn(
                name: "DueDate",
                table: "Reminders");

            migrationBuilder.DropColumn(
                name: "Location",
                table: "Reminders");

            migrationBuilder.DropColumn(
                name: "Status",
                table: "Reminders");

            migrationBuilder.DropColumn(
                name: "TimeToDo",
                table: "Reminders");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Category",
                table: "Reminders",
                type: "text",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<DateOnly>(
                name: "CreatedDate",
                table: "Reminders",
                type: "date",
                nullable: false,
                defaultValue: new DateOnly(1, 1, 1));

            migrationBuilder.AddColumn<DateOnly>(
                name: "DueDate",
                table: "Reminders",
                type: "date",
                nullable: false,
                defaultValue: new DateOnly(1, 1, 1));

            migrationBuilder.AddColumn<string>(
                name: "Location",
                table: "Reminders",
                type: "text",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "Status",
                table: "Reminders",
                type: "text",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<int>(
                name: "TimeToDo",
                table: "Reminders",
                type: "integer",
                nullable: false,
                defaultValue: 0);
        }
    }
}
